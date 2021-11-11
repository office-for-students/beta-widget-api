import unittest

from course_fetcher import CourseFetcher


class TestTidyWidgetStats(unittest.TestCase):
    def test_employment_in_work_or_study_is_returned(self):
        expected_stats = {"employment": [{"aggregation_level": 14, "in_work_or_study": 95}], "nss": []}
        input_stats = {
            "employment": [
                {
                    "aggregation_level": 14,
                    "assumed_to_be_unemployed": 5,
                    "in_study": 80,
                    "in_work": 5,
                    "in_work_and_study": 5,
                    "in_work_or_study": 95,
                    "not_available_for_work_or_study": 0,
                    "number_of_students": 15,
                    "response_rate": 100,
                }
            ]
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    def test_multiple_employment_in_work_or_study_is_returned_as_empty_array(self):
        expected_stats = {
            "employment": [], "nss": []
        }
        input_stats = {
            "employment": [
                {
                    "aggregation_level": 14,
                    "assumed_to_be_unemployed": 5,
                    "in_study": 80,
                    "in_work": 5,
                    "in_work_and_study": 5,
                    "in_work_or_study": 95,
                    "not_available_for_work_or_study": 0,
                    "number_of_students": 15,
                    "response_rate": 100,
                },
                {
                    "aggregation_level": 14,
                    "assumed_to_be_unemployed": 5,
                    "in_study": 70,
                    "in_work": 5,
                    "in_work_and_study": 5,
                    "in_work_or_study": 85,
                    "not_available_for_work_or_study": 0,
                    "number_of_students": 15,
                    "response_rate": 100,
                },
            ]
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    def test_nss_question_1_returned(self):
        expected_stats = {
            "nss": [
                {
                    "question_1": {
                        "description": "Staff are good at explaining things",
                        "agree_or_strongly_agree": 79,
                    }
                }
            ],
            "employment": [],
        }
        input_stats = {
            "nss": [
                {
                    "question_1": {
                        "description": "Staff are good at explaining things",
                        "agree_or_strongly_agree": 79,
                    }
                }
            ],
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    def test_multiple_nss_question_1_returned_as_empty_array(self):
        expected_stats = {
            "nss": [], "employment": []
        }

        input_stats = {
            "nss": [
                {
                    "question_1": {
                        "description": "Staff are good at explaining things",
                        "agree_or_strongly_agree": 79,
                    }
                },
                {
                    "question_1": {
                        "description": "Staff are good at explaining things",
                        "agree_or_strongly_agree": 93,
                    }
                },
            ]
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    def test_nss_question_27_returned(self):
        expected_stats = {
            "nss": [
                {
                    "question_27": {
                        "description": "Overall, I am satisfied with the quality of the course",
                        "agree_or_strongly_agree": 84,
                    }
                }
            ],
            "employment": []
        }
        input_stats = {
            "nss": [
                {
                    "question_27": {
                        "description": "Overall, I am satisfied with the quality of the course",
                        "agree_or_strongly_agree": 84,
                    }
                }
            ]
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    def test_multiple_nss_question_27_returned_as_empty_array(self):
        expected_stats = {
            "nss": [], "employment": []
        }

        input_stats = {
            "nss": [
                {
                    "question_27": {
                        "description": "Overall, I am satisfied with the quality of the course",
                        "agree_or_strongly_agree": 84,
                    }
                },
                {
                    "question_27": {
                        "description": "Overall, I am satisfied with the quality of the course",
                        "agree_or_strongly_agree": 73,
                    }
                },
            ]
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)

    # All being question 1 and 27 from nss and in_work_or_Study from employment
    def test_all_stats_returned(self):
        expected_stats = {
            'nss': [
            {
                'question_1': {
                    'description': 'Staff are good at explaining things', 
                    'agree_or_strongly_agree': 79
                }, 
                'question_27': {
                    'description': 'Overall, I am satisfied with the quality of the course', 
                    'agree_or_strongly_agree': 84
                }
            }], 
            'employment': [
                {
                    'aggregation_level': 14, 
                    'in_work_or_study': 95
                }
            ]
        }
        input_stats = {
            "nss": [
                {
                    "question_1": {
                        "description": "Staff are good at explaining things",
                        "agree_or_strongly_agree": 79,
                    },
                    "question_2": {
                        "description": "Staff have made the subject interesting",
                        "agree_or_strongly_agree": 100,
                    },
                    "question_3": {
                        "description": "The course is intellectually stimulating",
                        "agree_or_strongly_agree": 79,
                    },
                    "question_4": {
                        "description": "My course has challenged me to achieve my best work",
                        "agree_or_strongly_agree": 89,
                    },
                    "question_27": {
                        "description": "Overall, I am satisfied with the quality of the course",
                        "agree_or_strongly_agree": 84,
                    },
                }
            ],
            "employment": [
                {
                    "aggregation_level": 14,
                    "assumed_to_be_unemployed": 5,
                    "in_study": 80,
                    "in_work": 5,
                    "in_work_and_study": 5,
                    "in_work_or_study": 95,
                    "not_available_for_work_or_study": 0,
                    "number_of_students": 15,
                    "response_rate": 100,
                }
            ],
        }

        output_course = CourseFetcher.tidy_widget_stats(input_stats)
        self.assertEqual(expected_stats, output_course)
