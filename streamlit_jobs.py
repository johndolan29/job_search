import streamlit as st
import pandas as pd
import altair as alt
from utils import truncate_string, load_config
from processing_utils import post_processing, get_top_jobs
from streamlit_modal import Modal

config = load_config("config.yaml")
config["job_titles"] = (
    config["desired_job_titles"] + config["acceptable_job_titles"]
)

st.markdown(
    """
    <style>
    /* Remove top whitespace */
    div.block-container { padding-top: 1rem }
    </style>
    """,
    unsafe_allow_html=True,
)


#################
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_process_data(file_path, config):
    full_data = pd.read_csv(file_path)
    full_data['date_posted'] = full_data['date_posted'].str[:10]
    full_data["date_posted"] = pd.to_datetime(
        full_data["date_posted"], format="%Y-%m-%d", errors='coerce'
    )
    #full_data["rundate"] = pd.to_datetime(
    #    full_data["rundate"], format="%d/%m/%Y"
    #)
    full_data["rundate"] = pd.to_datetime(full_data["rundate"], errors="coerce", format="%d/%m/%Y")
    max_date = full_data["date_posted"].max()
    #max_date = (
    #	    full_data[full_data.rundate.dtype == "datetime64[ns]"]["rundate"]
    #	    .max()
    #	)

    full_data = post_processing(full_data, config)
    latest_data = full_data[full_data["rundate"].dt.date == max_date.date()]
    top_jobs, _ = get_top_jobs(
        latest_data, config["columns_list"], threshold=3
    )

    # Truncate values
    mapping = {
        "title": truncate_string,
        "company": truncate_string,
        "location": truncate_string,
        "industry": truncate_string,
    }

    latest_data = latest_data.apply(
        lambda x: x.apply(
            lambda y: (mapping[x.name](y) if x.name in mapping else y)
        )
    )

    # Make links clickable
    top_jobs["job_url"] = top_jobs["job_url"].apply(
        lambda x: (
            f'<a href="{x}" target="_blank">Link</a>'
            if pd.notnull(x)
            else "No URL"
        )
    )

    top_jobs.loc[top_jobs["description"].isna(), "description"] = (
        "No description available"
    )

    # make sure there are no weird characters in the description
    top_jobs["description"] = (
        top_jobs["description"]
        .astype(str)
        .apply(lambda x: x.encode("ascii", "ignore").decode("ascii"))
    )

    top_jobs["date_posted"] = top_jobs["date_posted"].dt.strftime("%Y-%m-%d")
    top_jobs["is_remote"] = top_jobs["is_remote"].map(
        {True: "Yes", False: "No"}
    )

    return full_data, top_jobs


file_path = config["filename"]
full_data, top_jobs = load_and_process_data(file_path, config)

<<<<<<< Updated upstream
#latest_rundate = full_data["rundate"].max().strftime("%Y-%m-%d")
latest_rundate = (
    full_data["rundate"]
=======
latest_rundate = (
    full_data[full_data.rundate.dtype == "datetime64[ns]"]["rundate"]
>>>>>>> Stashed changes
    .max()
    .strftime("%Y-%m-%d")
)

#################
st.title(f"Top Jobs Dashboard - {latest_rundate}")

page = st.radio(
    "Choose a page", ["Job Listings", "Time Series Analysis"], horizontal=True
)

if page == "Job Listings":
    st.subheader("Job Listings")

    cols_to_show = [
        "site",
        "title",
        "company",
        "salary",
        "location",
        "industry",
        "is_remote",
        "date_posted",
        "job_url",
        "score",
        "description",
    ]

    # Header row
    header_cols = st.columns(len(cols_to_show))
    headers = [
        "Site",
        "Title",
        "Company",
        "Salary",
        "Location",
        "Industry",
        "Is_remote",
        "Date_posted",
        "Job_url",
        "Score",
        "Description",
    ]
    for col_obj, col_name in zip(header_cols, headers):
        col_obj.markdown(f"**{col_name}**")

    # Initialize Modal
    modal = Modal(key="description_modal", title="Job Description")

    for i, row in top_jobs.iterrows():
        row_cols = st.columns(len(cols_to_show))
        for j, col_name in enumerate(cols_to_show):
            if col_name == "description":
                if row_cols[j].button("View Description", key=f"desc_btn_{i}"):
                    st.session_state["current_description"] = row[
                        "description"
                    ]
                    modal.open()
            elif col_name == "job_url":
                row_cols[j].markdown(row["job_url"], unsafe_allow_html=True)
            else:
                val = row[col_name] if pd.notnull(row[col_name]) else ""
                row_cols[j].write(val)

    # Display the modal if open
    if modal.is_open():
        with modal.container():
            st.write(
                st.session_state.get(
                    "current_description", "No description available"
                )
            )
            if st.button("Close"):
                # The modal will close on rerun if we don't call modal.open() again
                st.rerun()


elif page == "Time Series Analysis":
    job_counts = (
        full_data.drop_duplicates(subset=['title', 'company', 'date_posted', 'location' ])
        .groupby("date_posted")
        .size()
        .reset_index(name="count")
    )
    job_counts["date_posted"] = pd.to_datetime(job_counts["date_posted"], format='mixed')
    print(job_counts)

    chart = (
        alt.Chart(job_counts)
        .mark_bar()
        .encode(
            x=alt.X("date_posted:T", title="Date Posted"),
            y=alt.Y("count:Q", title="Number of Jobs"),
            tooltip=["date_posted", "count"],
        )
        .properties(
            width=1200, height=300, title="Number of Jobs Posted Over Time"
        )
    )

    st.altair_chart(chart, use_container_width=True)
