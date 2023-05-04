import json
import logging


class CourseFetcher:
    """Handles retrieving courses from Cosmos DB"""

    def __init__(self, client, collection_link):
        self.client = client
        self.collection_link = collection_link

    def get_course(self, version, institution_id, course_id, mode):
        """Retrieves a course document from Cosmos DB.

        Queries the Cosmos DB container for a course using the
        arguments passed in. If a course is found, it removes
        the additonal fields Cosmos DB added before returning it
        to the caller. If no course is found it returns None.

        """

        # Query the course container using the sql query and options
        courses_list = list(
            self.search_with_pub_ukprn(
                institution_id=institution_id, course_id=course_id, mode=mode, version=version
            )
        )

        # If no course matched the arguments passed in return None
        if not len(courses_list):
            courses_list = self.force_ukprn(institution_id, course_id, mode, version)
            if not len(courses_list):
                return None

        # Log an error if more than one course is returned by query.
        if len(courses_list) > 1:
            # Something's wrong; there should be only one matching course.
            course_count = len(courses_list)
            logging.error(f"{course_count} courses returned. There should be only one.")

        # Get the course from the list.
        course = courses_list[0]["widget"]
        # Remove unnecessary keys from the course.
        course["multiple_subjects"] = self.check_multiple_subjects(course["statistics"])
        stats = CourseFetcher.tidy_widget_stats(course["statistics"])
        course["statistics"] = stats
        # Convert the course to JSON and return
        return json.dumps(course)

    def force_ukprn(self, institution_id: int, course_id: int, mode: int, version):
        ukprn_search = list(self.search_with_ukprn(institution_id=institution_id, course_id=course_id, mode=mode,
                                                   version=version))
        pub_ukprn = ukprn_search[0]["widget"]["pub_ukprn"]
        courses_list = list(
            self.search_with_pub_ukprn(institution_id=pub_ukprn, course_id=course_id, mode=mode, version=version)
        )
        return courses_list

    def search_with_ukprn(self, institution_id: int, course_id: int, mode: int, version):
        """Searches with ukprn then uses the pubukprn to search correctly"""
        query = (
            'SELECT {"institution_id": c.course.institution.ukprn, "pub_ukprn": c.course.institution.pub_ukprn, "course_id": c.course_id, "course_mode": c.course_mode} AS widget from c '
            f"where c.course.institution.ukprn = '{institution_id}' "
            f"and c.course_id = '{course_id}' "
            f"and c.course_mode = {mode} "
            f"and c.version = {version} "
        )
        logging.info(f"obtaining pubukprn with ukprn")
        return self.fetch_from_cosmos(query)

    def search_with_pub_ukprn(self, institution_id: int, course_id: int, mode: int, version):
        query = (
            'SELECT {"institution_id": c.course.institution.pub_ukprn, "pub_ukprn": c.course.institution.pub_ukprn, "course_id": c.course_id, "course_name": {"english": c.course.title.english, "welsh": c.course.title.welsh}, "course_mode": c.course_mode, "institution_name":{"english": c.course.institution.pub_ukprn_name, "welsh": c.course.institution.pub_ukprn_welsh_name}, "statistics": { "employment": c.course.statistics.employment, "nss": c.course.statistics.nss} } AS widget from c '
            f"where c.course.institution.pub_ukprn = '{institution_id}' "
            f"and c.course_id = '{course_id}' "
            f"and c.course_mode = {mode} "
            f"and c.version = {version} "
        )
        logging.info(f"query: {query}")
        return self.fetch_from_cosmos(query)

    def fetch_from_cosmos(self, query):
        options = {"enableCrossPartitionQuery": True}
        return self.client.QueryItems(self.collection_link, query, options)

    @staticmethod
    def check_multiple_subjects(course) -> bool:
        return len(course["employment"]) > 1 or len(course["nss"]) > 1

    @staticmethod
    def tidy_widget_stats(data):
        """Removes wanted stats in response"""
        employment = data.get("employment", [])
        e = []
        if len(employment) > 0:
            i = dict()
            stats = ["aggregation_level", "in_work_or_study", "subject"]
            item = employment[0]
            for stat in stats:
                if stat in item:
                    i[stat] = item[stat]
            e.append(i)
        data["employment"] = e

        nss = data.get("nss", [])
        n = []
        if len(nss) > 0:
            j = dict()
            item = nss[0]
            stats = ["question_1", "question_27", "subject", "aggregation_level"]
            for stat in stats:
                if stat in item:
                    j[stat] = item[stat]
            n.append(j)
        data["nss"] = n
        return data
