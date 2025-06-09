#  Mobile Banking App Review Analysis – Week 2 Challenge

## Project Overview

This project simulates the role of a **Data Analyst at Omega Consultancy**, where the objective is to analyze **customer satisfaction** with mobile banking apps in Ethiopia by collecting and analyzing user reviews from the **Google Play Store**.

###  Business Objective

Help three major Ethiopian banks improve their mobile applications by:

- Collecting user reviews
- Analyzing sentiment and common themes
- Identifying satisfaction drivers and pain points
- Delivering actionable insights and recommendations

###  Target Apps

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

---

##  Timeline

| Milestone            | Date & Time (UTC)             |
|----------------------|-------------------------------|
| Challenge Intro       | Wed, 04 June 2024 – 8:00 AM   |
| Interim Submission    | Sun, 08 June 2024 – 8:00 PM   |
| Final Submission      | Tue, 10 June 2024 – 8:00 PM   |

---

##  Tasks and Deliverables

###  Task 1: Data Collection & Preprocessing

- Scrape 400+ reviews from Google Play for each bank using `google-play-scraper`
- Clean and preprocess data (remove duplicates, normalize dates)
- Save to CSV: `review`, `rating`, `date`, `bank`, `source`
- Commit code to the `task-1` branch

**KPI:** 1,200+ reviews with <5% missing data

---

###  Task 2: Sentiment & Thematic Analysis

- Perform sentiment analysis using models like `VADER`, `TextBlob`, or `distilBERT`
- Extract keywords using `spaCy` or `TF-IDF`
- Cluster into 3–5 themes per bank (e.g., UI, reliability)
- Save analysis results to CSV
- Commit to `task-2` branch and merge via PR

**KPI:** Sentiment scores for 90%+ reviews, 3+ themes per bank

---

###  Task 3: Store Data in Oracle DB

- Set up Oracle XE and create `bank_reviews` database
- Define schema: `banks`, `reviews`
- Insert cleaned data via Python scripts

**KPI:** Oracle DB populated with 1,000+ entries, SQL dump pushed to GitHub

---

###  Task 4: Insights & Recommendations

- Identify key **drivers** (e.g., fast login) and **pain points** (e.g., app crashes)
- Create visualizations using `matplotlib`, `seaborn`, `wordcloud`
- Compile a stakeholder-friendly **final report** with plots and insights

**Minimum Requirements:**

- 1 driver and 1 pain point per bank
- At least 2 plots
- 4–7 page final report (in Medium article style)

---

##  Scenarios

- **Scenario 1:** User Retention – Investigate app loading complaints
- **Scenario 2:** Feature Enhancement – Extract desired features
- **Scenario 3:** Complaint Management – Cluster support-related issues

---

##  Tech Stack

| Area                  | Tools / Libraries                          |
|-----------------------|---------------------------------------------|
| Web Scraping          | `google-play-scraper`                      |
| Preprocessing         | `pandas`, `datetime`, `re`                 |
| Sentiment Analysis    | `VADER`, `TextBlob`, `transformers`        |
| NLP & Theming         | `spaCy`, `sklearn`, `TF-IDF`               |
| Database              | `Oracle XE`, `cx_Oracle`                   |
| Visualization         | `matplotlib`, `seaborn`, `wordcloud`       |
| Version Control       | `Git`, `GitHub`                            |
| Reporting             | Markdown, PDF, or Medium-format write-up   |

---

 

