from utils import (
    extract_salary,
    extract_days_per_week,
    convert_salary_to_float,
)
import re


def post_processing(jobs_df, config):
    jobs_df["score"] = 0
    jobs_df["score"] = jobs_df["score"].astype(float)

    ###########

    jobs_df["industry"] = jobs_df["description"].str.extract(
        "(" + "|".join(config["industry_keywords"]) + ")", flags=re.IGNORECASE
    )
    jobs_df["industry"] = jobs_df["industry"].str.lower()

    ###########

    jobs_df["salary"] = jobs_df["description"].apply(extract_salary)
    jobs_df["days_per_week"] = jobs_df["description"].apply(
        extract_days_per_week
    )


    jobs_df["is_remote"] = jobs_df.apply(
        lambda row: (True if row["is_remote"] else False),
        axis=1,
    )

    # if 'salary' is null, fill it with the min_amount column
    jobs_df["salary"] = jobs_df["salary"].fillna(jobs_df["min_amount"])
    jobs_df["salary"] = jobs_df["salary"].fillna(jobs_df["max_amount"])

    jobs_df = jobs_df.reset_index(drop=True)

    jobs_df["salary"] = jobs_df.salary.apply(convert_salary_to_float)

    ###########

    # add score of 1 for each job title that matches the config
    for job_title in config["desired_job_titles"]:
        if job_title in jobs_df["title"].values:
            jobs_df.loc[
                jobs_df["title"].str.contains(job_title, case=False), "score"
            ] += 1
            break

    for job_title in config["acceptable_job_titles"]:
        if job_title in jobs_df["title"].values:
            jobs_df.loc[
                jobs_df["title"].str.contains(job_title, case=False), "score"
            ] += 0.5
            break

    # if non of the job titles match, subtract 1 from the score
    jobs_df.loc[
        (
            jobs_df["title"].str.contains(
                "|".join(config["job_titles"]), case=False
            )
            == False
        ),
        "score",
    ] -= 1

    # add score of 1 if the job is remote
    # jobs_df.loc[jobs_df["is_remote"], "score"] += 1

    # add score of 1 if nice_to_have_keywords are in the description
    for keyword in config["nice_to_have_keywords"]:
        jobs_df.loc[
            (jobs_df["description"].notna())
            & (jobs_df["description"].str.contains(keyword, case=False)),
            "score",
        ] += 1

    # add score of 1 if location matches the config location
    for location in config["locations"]:
        jobs_df.loc[
            (jobs_df["location"].notna())
            & (jobs_df["location"].str.contains(location, case=False)),
            "score",
        ] += 1

    jobs_df.loc[
        (jobs_df["days_per_week"].notna()) & (jobs_df["days_per_week"] <= 2),
        "score",
    ] += 1

    jobs_df.loc[
        (jobs_df["salary"] > config["min_salary"]),
        "score",
    ] += 1

    ###########

    # remove jobs that contain the 'non_job_titles_keywords'
    for keyword in config["non_job_title_keywords"]:
        jobs_df = jobs_df[
            ~jobs_df["title"].str.contains(keyword, case=False, na=False)
        ]

    # remove jobs with USD currency
    jobs_df = jobs_df[~jobs_df["currency"].astype(str).str.contains("USD", na=False)]

    jobs_df.sort_values(by="score", ascending=False, inplace=True)

    return jobs_df


def get_top_jobs(jobs_df, columns_list, threshold=2):
    must_have_in_job_title = "Data Scie"
    must_have_in_job_title = must_have_in_job_title.lower()
    data_science_jobs = jobs_df[
        jobs_df["title"].str.lower().str.contains(must_have_in_job_title)
    ]

    top_jobs = data_science_jobs[data_science_jobs.score >= threshold][
        columns_list
    ]

    return top_jobs, data_science_jobs
