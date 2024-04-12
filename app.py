import streamlit as st
import requests
import time
from datetime import datetime

# --- Secrets Management (Follow Streamlit Docs) ---
keboola_token = st.secrets["keboola_token"]

# --- User Input ---
config_id = st.secrets["config_id"]

# UI
section_main = st.container()
section_main.title("Trigger Keboola Job")


# --- API Request Functions ---
def create_keboola_job(config_id, token):
    url = "https://queue.keboola.com/jobs"
    headers = {"X-StorageApi-Token": token}
    data = {
        "component": "keboola.orchestrator",
        "mode": "run",
        "config": config_id,
        "tag": "latest"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        st.error("Job creation failed. Check configuration ID and token.")
        return None

def get_job_status(job_id, token):
    url = f"https://queue.keboola.com/jobs/{job_id}"
    headers = {"X-StorageApi-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_job_information(job_data):
    """Displays essential information from the Keboola job response.
    Args:
        job_data (dict): The JSON response from the Keboola API.
    """
    
    job_status = job_data["status"]

    # Header
    section_main.subheader(f"Job ID: {job_data['id']}")
    if job_status == "terminated":
        section_main.warning('Job Terminated!', icon="⚠️")
    elif job_status == "error":
        section_main.error('Job Error', icon="🚨")
    elif status["status"] == "success":
        section_main.success('Job Success!', icon="✅")
    #section_main.subheader(f"Status: {job_data['status']}")

    start_time = datetime.strptime(job_data['startTime'][:19], "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(job_data['endTime'][:19], "%Y-%m-%dT%H:%M:%S")
    start = start_time.strftime("%H:%M:%S")
    end = end_time.strftime("%H:%M:%S")
    
    # Columns
    col1, col2, col3 = section_main.columns(3)
    col1.metric(label="START", value=start)
    col2.metric(label="END", value=end)
    col3.metric(label="DURATION (s)", value=job_data.get('durationSeconds', 'Not Yet Completed'))
    
    section_main.subheader("Message:")
    section_main.write(job_data['result']['message'])
    

      
# --- Job Creation and Polling ---
if st.button("Trigger Job"):
    job_id = create_keboola_job(config_id, keboola_token)
    if job_id:
        st.toast("Job Started!", icon='🐙')
        with st.spinner("Waiting for job to complete..."):
            while True:
                status = get_job_status(job_id, keboola_token)
                if status["status"] == "terminated":
                    display_job_information(status)
                    break
                elif status["status"] == "success":
                    display_job_information(status)
                    break
                elif status["status"] == "error":
                    display_job_information(status)
                    break
                time.sleep(5)  # Adjust the polling interval as needed

        # Display job details
        job_details = get_job_status(job_id, keboola_token)
