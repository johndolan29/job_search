from utils import (
    load_config,
    make_clickable,
    truncate_string,
)
from processing_utils import (
    post_processing,
    get_top_jobs,
)
from jobspy import scrape_jobs
import pandas as pd

from itertools import product
import os
import time

config = load_config(
    "/home/pi/job_search/config.yaml"
)
default_location = config["default_location"]

jobs_dict_list = [
    {
        "job_title": job_title,
        "is_remote": is_remote,
        "location": location,
        "distance": distance,
    }
    for job_title, is_remote, location, distance in product(
        config["search_job_titles"],
        config["remote_list"],
        config["search_locations"],
        config["distances"],
    )
]

config["job_titles"] = (
    config["desired_job_titles"] + config["acceptable_job_titles"]
)

today = pd.Timestamp.now().strftime("%d/%m/%Y")
filename = config["filename"]


# if remote job, set location to default_location
for job in jobs_dict_list:
    if job["is_remote"]:
        job["location"] = default_location

# remove duplicates
jobs_dict_list = [dict(t) for t in {tuple(d.items()) for d in jobs_dict_list}]


def run_jobs_search(jobs_dict_list):
    jobs_dfs = []

    for job_dict in jobs_dict_list:
        print(job_dict)

        google_search_term = (
            job_dict["job_title"] + " near " + job_dict["location"]
            if not job_dict["is_remote"]
            else job_dict["job_title"] + " remote UK"
        )

        jobs = scrape_jobs(
            site_name=["indeed", "google", "linkedin"],
            search_term=job_dict["job_title"],
            google_search_term=google_search_term,
            location=job_dict["location"],
            distance=job_dict["distance"],
            results_wanted=100,
            hours_old=24 * 7,
            country_indeed="UK",
            is_remote=job_dict["is_remote"],
            linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower),
            verbose=False,
        )

        jobs_dfs.append(jobs)
        time.sleep(60*30)

    jobs_df = pd.concat(jobs_dfs)

    jobs_df = jobs_df.drop_duplicates(subset=["id"])
    jobs_df = jobs_df.drop(columns=["company_logo"])
    jobs_df["date_posted"] = pd.to_datetime(
        jobs_df["date_posted"], format="%d/%m/%Y"
    )
    jobs_df["rundate"] = str(today)
    return jobs_df


if not os.path.exists(filename):
    jobs_df = run_jobs_search(jobs_dict_list)
    jobs_df.to_csv(filename, index=False)
else:
    existing_jobs_df = pd.read_csv(filename)
    unique_dates = existing_jobs_df["rundate"].unique()
    if today in unique_dates:
        print("Jobs already fetched today")
        jobs_df = existing_jobs_df
    else:
        print("Fetching jobs")
        jobs_df = pd.concat(
            [existing_jobs_df, run_jobs_search(jobs_dict_list)]
        )
        jobs_df.to_csv(filename, index=False)
