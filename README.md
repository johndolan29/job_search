# Job Searcher

This repository provides a streamlined tool for job searching, using the `jobspy` library for scraping jobs and a user-friendly Streamlit-based dashboard for visualization. It is designed to simplify the process of finding relevant jobs, post-processing data, and analysing trends over time.

---

## Features

- **Automated Job Scraping**:
  - Searches across multiple platforms (`Indeed`, `Google`, `LinkedIn`) based on configurable parameters like job titles, locations, remote work, and search radius.
  - Saves job data to a CSV file for persistent storage.

- **Streamlit Dashboard**:
  - **Job Listings**: Displays the top job opportunities in an interactive table format.
  - **Time Series Analysis**: Visualizes trends in job postings over time using Altair charts.

- **Post-Processing**:
  - Cleans and preprocesses job data for better usability.
  - Highlights "top jobs" based on predefined scoring thresholds.

---

## Installation

### Prerequisites
- Python 3.10 or above
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `altair`
  - `jobspy`
  - `streamlit-modal`

Install dependencies using pip:
```bash
pip install -r requirements.txt
```

### Configuration
Create a config.yaml file in the root directory with the following structure:
```
search_job_titles: [ "Data Scientist", "Machine Learning Engineer" ]
desired_job_titles: [ "Senior Data Scientist" ]
acceptable_job_titles: [ "Data Analyst" ]
remote_list: [ true, false ]
search_locations: [ "London, UK", "Manchester, UK" ]
distances: [50] # miles
default_location: "Leeds, UK"
filename: "jobs_data.csv"
columns_list: [ "title", "company", "salary", "location", "industry", "score" ]
```
Update paths and parameters based on your requirements.

### Usage:
1. Scrape Jobs:
    Run the jobs_search.py script to scrape job postings and save the results:
    ```
    python jobs_search.py
    ```
    This script:
    - Reads configurations from config.yaml.
    - Scrapes job postings based on the defined criteria.
    - Saves the scraped data to a CSV file (jobs_data.csv).

2. Visualize Data
    Launch the Streamlit dashboard using the streamlit_jobs.py script:
    ```
    streamlit run streamlit_jobs.py
    ```
    The dashboard includes:

    - *Job Listings*: Displays detailed job information, including clickable links and descriptions.
    - *Time Series Analysis*: Shows the number of jobs posted over time in a bar chart.

### Contributing
Contributions are welcome! Please feel free to submit a pull request or raise issues for bug fixes and feature requests.