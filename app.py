import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Advancement Prospect Search")
st.write("Natural-language search over advancement contact reports.")

@st.cache_data
def load_data():
    contacts = pd.read_csv(
        r"C:\Program Files\Projects\Fundraising Data set\kaggle_dataset\contacts.csv"
    )

    contacts["rag_text"] = (
        "Donor ID: " + contacts["Donor_ID"].astype(str) +
        "\nContact Date: " + contacts["Contact_Date"].astype(str) +
        "\nContact Type: " + contacts["Contact_Type"].astype(str) +
        "\nOutcome: " + contacts["Outcome_Category"].astype(str) +
        "\nReport: " + contacts["Report_Text"].astype(str)
    )

    return contacts

contacts = load_data()

@st.cache_resource
def build_vectorizer(texts):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = build_vectorizer(contacts["rag_text"])

def prospect_search(query, top_k=10, min_score=0.05):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    if similarities.max() < min_score:
        return pd.DataFrame()

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = contacts.iloc[top_indices][
        ["Donor_ID", "Contact_Date", "Contact_Type", "Outcome_Category", "Report_Text"]
    ].copy()

    results["similarity_score"] = similarities[top_indices]

    return results

query = st.text_input("Search contact reports", placeholder="e.g., interested in scholarships")

top_k = st.slider("Number of results", 5, 25, 10)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        results = prospect_search(query, top_k=top_k)

        if results.empty:
            st.error("No relevant contact reports found.")
        else:
            st.success(f"Found {len(results)} relevant contact reports.")
            st.dataframe(results)