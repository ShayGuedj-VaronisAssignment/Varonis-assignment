# Azure DevOps Work Item Management

This project is a Python application that interacts with Azure DevOps to retrieve recent work items, update their titles, and create child work items for Product Backlog Items (PBIs). It utilizes the Azure DevOps REST API for querying and modifying work items by updating titles with the current date to the titeles of existing work items.

## Prerequisites

- Python 3.9 or higher
- Docker
- An Azure DevOps organization and project
- A Personal Access Token (PAT) with appropriate permissions to access work items

## Installation

### Local Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/ShayGuedj-VaronisAssignment/Varonis-assignment.git
   cd Varonis-assignment
   ```
2. Create a virtual environment (optional but recommended):
   ``` bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ``` bash
   pip install -r requirements.txt
   ```
4. Edit the .env file in the root directory and add your Azure DevOps configuration (the credentials I gave are expired so I left them in the file).

## Docker Setup

1. Build the Docker image:
   ``` bash
   docker build -t azure-devops-work-item-management .
   ```
2. Run the Docker container:
   ``` bash
   docker run --env-file .env azure-devops-work-item-management
   ```

## Usage

1. The script automatically retrieves work items created in the last 3 days. If there are recent work items, it will display their details.
2. If no recent work items are found, it will retrieve all existing work items, update their titles to include the current date, and create child work items for each Product Backlog Item.
3. You can modify the script to change how work items are queried or processed based on your needs.

## Important Notes

* Make sure your PAT has the necessary permissions to read and write work items in Azure DevOps.
* The script uses the requests library to make API calls to Azure DevOps, so ensure you have an active internet connection.

## License

This project is licensed under the MIT License. See the LICENSE file for details.





