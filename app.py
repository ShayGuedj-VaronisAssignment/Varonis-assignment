import requests
from datetime import datetime, timedelta
import base64
import os
from dotenv import load_dotenv

# Import the environment variables from .env file in the same directory
load_dotenv()

# Environment variables
organization = os.getenv('AZURE_DEVOPS_ORG')
project = os.getenv('AZURE_DEVOPS_PROJECT')
pat = os.getenv('AZURE_DEVOPS_PAT')
encoded_pat = base64.b64encode(f':{pat}'.encode()).decode()
base_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql'
api_version = '6.0'  # I got an error about the version so I had to specify the version to fix it.

# Get work items created in the last 3 days
def get_recent_work_items():
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    query = f"SELECT [System.Id], [System.Title], [System.WorkItemType], [System.CreatedDate] FROM WorkItems WHERE [System.CreatedDate] >= '{three_days_ago}'"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}',
        'Accept': f'application/json; api-version={api_version}'
    }
    response = requests.post(f'{base_url}?api-version={api_version}', json={'query': query}, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        return response.json()['workItems']
    else:
        return []

# Get all work items and not only work items from the past 3 days
# This function was written more for testing as my project has no work items (new project)
def get_all_work_items():
    query = "SELECT [System.Id], [System.Title], [System.WorkItemType] FROM WorkItems"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}',
        'Accept': f'application/json; api-version={api_version}'
    }
    response = requests.post(f'{base_url}?api-version={api_version}', json={'query': query}, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        return response.json()['workItems']
    else:
        return []

# Append current date to the title of PBIs/Features/Bugs
def update_work_item_titles(work_items):
    current_date = datetime.now().strftime('%Y-%m-%d')
    for work_item in work_items:
        wi_id = work_item['id']
        wi_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{wi_id}?api-version={api_version}'
        headers = {
            'Content-Type': 'application/json-patch+json',
            'Authorization': f'Basic {encoded_pat}',
            'Accept': f'application/json; api-version={api_version}'
        }
        data = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": f"{work_item['fields']['System.Title']} - {current_date}"
            }
        ]
        requests.patch(wi_url, json=data, headers=headers)

# Create child work items for each PBI
def create_child_work_items(work_items):
    for work_item in work_items:
        if work_item['fields']['System.WorkItemType'] == 'Product Backlog Item':
            child_data = [
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": f"Child of {work_item['fields']['System.Title']}"
                },
                {
                    "op": "add",
                    "path": "/relations/-",
                    "value": {
                        "rel": "System.LinkTypes.Hierarchy-Forward",
                        "url": f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item['id']}?api-version={api_version}",
                        "attributes": {
                            "comment": "Making a child link"
                        }
                    }
                }
            ]
            headers = {
                'Content-Type': 'application/json-patch+json',
                'Authorization': f'Basic {encoded_pat}',
                'Accept': f'application/json; api-version={api_version}'
            }
            requests.post(f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version={api_version}', json=child_data, headers=headers)

if __name__ == "__main__":
    recent_work_items = get_recent_work_items()
    if recent_work_items:
        print("Displaying work items created in the last 3 days:")
        for wi in recent_work_items:
            print(f"ID: {wi['id']}, Title: {wi['fields']['System.Title']}, Created Date: {wi['fields']['System.CreatedDate']}")
    else:
        print("No work items created in the last 3 days. Proceeding with the existing logic.")
        work_items = get_all_work_items()
        update_work_item_titles(work_items)
        create_child_work_items(work_items)
