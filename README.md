# Prospect Intelligence Dashboard

## Live App

https://cnkwog6owmqmiahkiimqhm.streamlit.app/

## Business Problem

The central question for this project is:

**Who deserves advancement attention, and why?**

Rather than simply predicting who may give again, this dashboard is designed to help advancement and fundraising teams prioritize prospects based on capacity, affinity, engagement, and timing signals.

## Project Overview

This project creates a Prospect Intelligence Dashboard using a synthetic fundraising dataset. The dashboard segments constituents into three actionable groups:

1. **Major Gift Candidates**
   High-capacity, high-affinity prospects who appear ready for major gift qualification.

2. **Emerging Prospects**
   Prospects with positive giving momentum and engagement signals who may be moving toward greater giving potential.

3. **Re-engagement Opportunities**
   Historically valuable donors who have not given recently and may be candidates for renewed outreach or stewardship.

   <img width="956" height="496" alt="image" src="https://github.com/user-attachments/assets/d7f14dfa-a217-42e3-86e7-1aeb2bddf2ee" />


## Methodology

The dashboard uses three core scoring dimensions:

### Capacity Signals

* Lifetime giving
* Largest gift
* Gift count
* Giving years
* Monetary score

### Affinity Signals

* Engagement score
* Event attendance
* Contact reports
* Recent engagement

### Timing Signals

* Recency of giving
* Recent giving amount
* Giving momentum
* Giving in the last 12 months

These signals are combined into a **Prospect Intelligence Score** designed to support prioritization rather than replace fundraiser judgment.

## Data Caveat

This project uses a synthetic fundraising dataset and does not contain real donor, alumni, or constituent data. The goal is to demonstrate a realistic advancement analytics workflow while preserving privacy and confidentiality.

## Tech Stack

* Python
* Pandas
* Streamlit
* GitHub
* Streamlit Community Cloud

## How to Run Locally

```bash
streamlit run prospect_intellegence_dashboard.py
```
