beta-widget-api
=================
Service to discoveruni widget access to course statistics.

This is a FastAPI app, that can also be run as an azure function.

Builds

master - [![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/prod/prod-widget-api?branchName=develop)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=41&branchName=develop)

develop - [![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/dev/dev-widget-api?branchName=develop)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=37&branchName=develop)

### Configuration Settings

Add the following to your local.settings.json:

| Variable                         | Default                | Description                                                        |
|----------------------------------|------------------------|--------------------------------------------------------------------|
| FUNCTIONS_WORKER_RUNTIME         | python                 | The programming language the function worker runs on               |
| AzureStorageAccountName          | {retrieve from portal} | The default endpoint to access storage account                     |
| AzureCosmosDbUri                 | {retrieve from portal} | The cosmos db uri to access the datastore                          |
| AzureCosmosDbKey                 | {retrieve from portal} | The cosmos database key in which to connect to the datastore       |
| AzureCosmosDbConnectionString    | {retrieve from portal} | The connection string in which to connect to the datastore         |
| AzureCosmosDbDatabaseId          | discoveruni            | The name of the database in which resource documents are stored in |
| AzureCosmosDbDataSetCollectionId | datasets               | The name of the collection in which datasets are uploaded to       |
| AzureCosmosDbCoursesCollectionId | courses                | The name of the collection in which courses are uploaded to        |
| ALLOWED_HOSTS                    | ""                     | The allowed hosts for the application as a comma separated string  |

### Setup

### Pre-Setup

1) Install [.Net Core 2.2 SDK](https://dotnet.microsoft.com/download), if you haven't already.
2) Install python 3.11

Mac user:

Install Python via (python.org)[https://python.org] or alternatively use brew

Windows user:

3. Make sure Python 3.8> is set on your PATH, you can check this by running `python -v` in terminal window.

4. Install Azure Client
```
Mac user:
brew tap azure/functions
brew install azure-functions-core-tools

Windows user:
```
5) Setup Visual Studio Code, install [visual studio code](https://code.visualstudio.com/)
6) Also install the following extensions for visual studio code - documentation [here](https://code.visualstudio.com/docs/editor/extension-gallery)

```
Python
Azure CLI Tools
Azure Account
Azure Functions
Azure Storage
```

7) Sign into Azure with Visual Studio Code - follow documentation [here](https://docs.microsoft.com/en-us/azure/azure-functions/tutorial-vs-code-serverless-python#_sign-in-to-azure)

#### Building resources and running azure function locally

1) Requires [beta-data-pipelines](https://github.com/office-for-students/beta-data-pipelines) to have been built and run once to load data into cosmos db

2) Retrieve all cosmos db environment variables (see configuration settings) from azure cosmos db instance that your widget API will be connecting to.

3) Retrieve the Azure Storage conection string from azure storage container instance.

4) Create your local.settings.json file at root level of repository and include all environment variables in the configuration settings table above.

5) Create a virtual machine to run the azure function application by running `python -m venv .env` at root level of repository.

6) Run service on virtual machine by doing the following:
```
source .env/bin/activate
pip install -r requirements.txt
func host start
OR
uvicorn main:app --reload
```

### Tests

To run tests, run the following command: `pytest -v`

### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.

# new function app creation

**NB** Current release is done outside the pipeline, so the function app is created manually.

Below is the command for creating the function app in the existing pre-prod account
`az functionapp create --resource-group <resource group> --consumption-plan-location <region> --runtime python --runtime-version 3.11 --functions-version 4 --name <app-name>
--storage-account <storage account> --os-type Linux`

# new function app deployment

Below is the command to deploy the function app to azure (pre-prod)

`func azure functionapp publish <app-name>`

These commands should be updated with the correct function app name and the correct resource group name for production.
