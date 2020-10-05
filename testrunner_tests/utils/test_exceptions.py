import unittest
from testrunner_tests.utils import utils
from testrunner_tests.tests import test_divider
from testrunner_tests.tests import clients


class ExceptionTest(unittest.TestCase):
    def test_unsupported_application_exception(self):
        self.assertRaises(Exception, test_divider.run_tests, 'ecs', 'http://127.0.0.1:5000', 'python')

    def test_webapp_endpoint_curl_exception(self):
        self.assertRaises(Exception, utils.invoke_and_get_traces_for_webapp, '')

    def test_lambda_endpoint_exception(self):
        self.assertRaises(Exception, utils.invoke_and_get_traces_for_lambda, 'test', '', clients.lambda_client)

    def test_segment_data_from_response_exception(self):
        self.assertRaises(Exception, utils.get_segment_data_from_response, '')
