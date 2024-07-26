from decouple import config

# Server
DEBUG = config("DEBUG", default=False, cast=bool)
BASE_URL = config("BASE_URL")
API_KEY = config("API_KEY", default="")
API_DOMAIN = config("API_DOMAIN", default="")
# ALLOWED ORIGINS example, "https://google.com, http://localhost:8000"
ALLOWED_ORIGINS = config('ALLOWED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])

# API
COURSE_DATA_SERVICE = config("CourseDataService")
COSMOSDB_URI = config("AzureCosmosDbUri")
COSMOSDB_KEY = config("AzureCosmosDbKey")
COSMOSDB_DATABASE_ID = config("AzureCosmosDbDatabaseId")
COSMOSDB_COURSES_COLLECTION_ID = config("AzureCosmosDbCoursesCollectionId")
COSMOSDB_INSTITUTION_COLLECTION_ID = config("AzureCosmosDbInstitutionsCollectionId")
COSMOSDB_DATASET_COLLECTION_ID = config("AzureCosmosDbDataSetCollectionId")
HARDCODED_HIGHEST_DATASET = config("HardcodedHighestDataset", default=None)