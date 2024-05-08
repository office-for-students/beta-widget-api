import logging
import os
import traceback
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from course_fetcher import CourseFetcher
from utils import get_collection_link, get_cosmos_client, get_http_error_response_json
# from dataset_helper import DataSetHelper
from course_param_validator import valid_course_params
from dataset_helper import get_highest_successful_version_number


from constants import COSMOSDB_URI
from constants import COSMOSDB_KEY
from constants import COSMOSDB_DATABASE_ID
from constants import COSMOSDB_COURSES_COLLECTION_ID
from constants import COSMOSDB_INSTITUTION_COLLECTION_ID
from constants import HARDCODED_HIGHEST_DATASET

app = FastAPI()
# app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')

# Intialise cosmos db client
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
        # logging.info(f"url: {req.url}")
        logging.info(f"route_params: {params}")

        # params = dict(req.route_params)

        #
        # The params are used in DB queries, so let's do
        # some basic sanitisation of them.
        #
        if not valid_course_params(params):
            logging.info(
                f'Parameter Error Invalid parameter passed {institution_id} {course_id} {mode}. Status code: 400')
            return {"message": f'Parameter Error Invalid parameter passed {institution_id} {course_id} {mode}',
                    "status_code": 400}

        logging.info("The parameters look good")

        courses_collection_link = get_collection_link(
            COSMOSDB_DATABASE_ID, COSMOSDB_COURSES_COLLECTION_ID
        )
        # dataset_collection_link = get_collection_link(
        #     COSMOSDB_DATABASE_ID, COSMOSDB_INSTITUTION_COLLECTION_ID
        # )

        # Intialise a CourseFetcher
        course_fetcher = CourseFetcher(client, courses_collection_link)

        # Initialise dataset helper - used for retrieving latest dataset version
        # dsh = DataSetHelper(client, dataset_collection_link)
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

        # Raise so Azure sends back the HTTP 500
        raise e
