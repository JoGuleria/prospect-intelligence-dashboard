import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Prospect Intelligence Dashboard",
    layout="wide"
)

# ============================================================
# Load Data
# ============================================================

output_folder = Path.home() / "Documents" / "prospect_intelligence_outputs"

major = pd.read_csv(output_folder / "top_50_major_gift_candidates.csv")
emerging = pd.read_csv(output_folder / "top_50_emerging_prospects.csv")
reengage = pd.read_csv(output_folder / "top_50_reengagement_opportunities.csv")

# ============================================================
# Helper Functions
# ============================================================

def format_currency(x):
    try:
        return "${:,.0f}".format(x)
    except:
        return x

def show_kpis(df, label):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Prospects", len(df))

    with col2:
        if "Lifetime_Giving" in df.columns:
            st.metric("Avg Lifetime Giving", format_currency(df["Lifetime_Giving"].mean()))

    with col3:
        if "Engagement_Score" in df.columns:
            st.metric("Avg Engagement", round(df["Engagement_Score"].mean(), 1))

    with col4:
        if "prospect_intelligence_score" in df.columns:
            st.metric("Avg Prospect Score", round(df["prospect_intelligence_score"].mean(), 1))


def clean_display(df):
    display_cols = [
        "ID",
        "Full_Name",
        "donor_type",
        "Constituent_Type_2",
        "Class_Year",
        "region",
        "Professional_Background",
        "Prospect_Stage",
        "Rating",
        "Lifetime_Giving",
        "largest_gift",
        "gift_count",
        "giving_years",
        "Engagement_Score",
        "event_count",
        "contact_count",
        "capacity_score",
        "affinity_score",
        "timing_score",
        "prospect_intelligence_score",
        "why_surfaced"
    ]

    display_cols = [c for c in display_cols if c in df.columns]
    out = df[display_cols].copy()

    money_cols = ["Lifetime_Giving", "largest_gift"]
    for col in money_cols:
        if col in out.columns:
            out[col] = out[col].apply(format_currency)

    score_cols = [
        "capacity_score",
        "affinity_score",
        "timing_score",
        "prospect_intelligence_score",
        "Engagement_Score"
    ]

    for col in score_cols:
        if col in out.columns:
            out[col] = out[col].round(1)

    return out


def filter_dataframe(df):
    filtered = df.copy()

    st.sidebar.subheader("Filters")

    if "region" in filtered.columns:
        regions = sorted(filtered["region"].dropna().unique())
        selected_regions = st.sidebar.multiselect(
            "Region",
            regions,
            default=regions
        )
        filtered = filtered[filtered["region"].isin(selected_regions)]

    if "donor_type" in filtered.columns:
        donor_types = sorted(filtered["donor_type"].dropna().unique())
        selected_types = st.sidebar.multiselect(
            "Donor Type",
            donor_types,
            default=donor_types
        )
        filtered = filtered[filtered["donor_type"].isin(selected_types)]

    if "Prospect_Stage" in filtered.columns:
        stages = sorted(filtered["Prospect_Stage"].dropna().unique())
        selected_stages = st.sidebar.multiselect(
            "Prospect Stage",
            stages,
            default=stages
        )
        filtered = filtered[filtered["Prospect_Stage"].isin(selected_stages)]

    return filtered


# ============================================================
# Dashboard Header
# ============================================================

st.title("Prospect Intelligence Dashboard")

st.write(
    """
    This dashboard identifies donors and prospects who deserve advancement attention
    based on capacity, affinity, engagement, timing, and giving behavior.
    """
)

st.markdown(
    """
    **Core question:** Who should we pay attention to?
    """
)

# ============================================================
# Sidebar Segment Selection
# ============================================================

segment = st.sidebar.radio(
    "Select Prospect Segment",
    [
        "Major Gift Candidates",
        "Emerging Prospects",
        "Re-engagement Opportunities"
    ]
)

if segment == "Major Gift Candidates":
    df = major
    description = """
    High-capacity and high-affinity prospects who appear most ready for major gift qualification.
    """
elif segment == "Emerging Prospects":
    df = emerging
    description = """
    Prospects with positive giving momentum and engagement signals who may be rising into future major gift potential.
    """
else:
    df = reengage
    description = """
    Historically valuable donors who appear inactive or under-engaged and may be candidates for reactivation.
    """

df_filtered = filter_dataframe(df)

# ============================================================
# Main View
# ============================================================

st.header(segment)
st.write(description)

show_kpis(df_filtered, segment)

st.subheader("Prospect List")

st.dataframe(
    clean_display(df_filtered),
    use_container_width=True,
    height=500
)

# ============================================================
# Download Button
# ============================================================

csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Current Prospect List",
    data=csv,
    file_name=f"{segment.lower().replace(' ', '_')}.csv",
    mime="text/csv"
)

# ============================================================
# Methodology
# ============================================================

with st.expander("Methodology"):
    st.write(
        """
        This dashboard uses three scoring dimensions:

        **Capacity Score**
        - Lifetime giving
        - Largest gift
        - Gift count
        - Giving years
        - Monetary score

        **Affinity Score**
        - Engagement score
        - Event attendance
        - Contact reports
        - Board role
        - Recent engagement

        **Timing Score**
        - Recency
        - Recent giving
        - Giving momentum
        - Giving in the last 12 months

        These are combined into a Prospect Intelligence Score designed to help
        advancement teams prioritize who deserves attention.
        """
    )