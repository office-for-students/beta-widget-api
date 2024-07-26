import logging
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from processes import constants
from processes.constants import COSMOSDB_COURSES_COLLECTION_ID
from processes.constants import COSMOSDB_DATABASE_ID
from processes.constants import COSMOSDB_KEY
from processes.constants import COSMOSDB_URI
from processes.course_fetcher import CourseFetcher
from processes.course_param_validator import valid_course_params
from processes.dataset_helper import get_highest_successful_version_number
from processes.utils import get_collection_link
from processes.utils import get_cosmos_client

app = FastAPI()
templates = Jinja2Templates(directory='templates')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise cosmos db client
client = get_cosmos_client(COSMOSDB_URI, COSMOSDB_KEY)


@app.get("/institutions/{institution_id}/courses/{course_id}/modes/{mode}")
async def main(institution_id: str, course_id: str, mode: str):
    """Implements the REST API endpoint for getting course documents.

    The endpoint implemented is:
        /institutions/{institution_id}/courses/{course_id}/modes/{mode}

    The API is fully documented in a swagger document in the same repo
    as this module.
    """

    try:
        params = {
            'institution_id': institution_id,
            'course_id': course_id,
            'mode': mode
        }
        logging.info("Process a request for a course.")

        logging.info(f"route_params: {params}")

        # The params are used in DB queries, so let's do
        # some basic sanitization of them.

        if not valid_course_params(params):
            logging.info(
                f'Parameter Error Invalid parameter passed {institution_id} {course_id} {mode}. Status code: 400')
            return {"message": f'Parameter Error Invalid parameter passed {institution_id} {course_id} {mode}',
                    "status_code": 400}

        logging.info("The parameters look good")

        courses_collection_link = get_collection_link(
            COSMOSDB_DATABASE_ID, COSMOSDB_COURSES_COLLECTION_ID
        )

        # Initialise a CourseFetcher
        course_fetcher = CourseFetcher(client, courses_collection_link)

        # Initialise dataset helper - used for retrieving latest dataset version
        version = get_highest_successful_version_number(COSMOSDB_URI, COSMOSDB_KEY)

        # Get the course
        course = course_fetcher.get_course(version=version, **params)

        if course:
            return {"status_code": 200, "data": course}
        else:
            logging.info('Course Error: course not found {institution_id} {course_id} {mode}. Status code: 400')
            return {"message": f"Course Error: course not found {institution_id} {course_id} {mode}",
                    "status_code": 400}

    except Exception as e:
        logging.error(traceback.format_exc())

        raise e
