import json, time
import requests

API = "https://clinicaltrials.gov/api/v2/studies"
AREAS = {"obesity": "obesity", "alzheimers": "alzheimer disease", "nsclc": "non-small cell lung cancer"}
FIELDS = ",".join(["NCTId", "OverallStatus", "WhyStopped", "Phase", "StartDate",
    "PrimaryCompletionDate", "EnrollmentCount", "EligibilityCriteria", "LocationFacility"])

def pull(condition, max_pages=20):
    params = {"query.cond": condition, "filter.overallStatus": "COMPLETED,TERMINATED",
              "fields": FIELDS, "pageSize": 1000, "countTotal": "true"}
    studies, page = [], 0
    while page < max_pages:
        r = requests.get(API, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        if page == 0:
            print(f"  total matching: {data.get('totalCount')}")
        studies += data.get("studies", [])
        token = data.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token
        page += 1
        time.sleep(0.5)
    return studies

for name, cond in AREAS.items():
    print(name)
    studies = pull(cond)
    with open(f"data/raw/{name}.json", "w") as f:
        json.dump(studies, f)
    print(f"  saved {len(studies)} studies")