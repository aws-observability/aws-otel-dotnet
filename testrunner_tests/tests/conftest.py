import os
import pytest
import pickle
import logging

from testrunner_tests.tests import clients


@pytest.fixture(scope='module')
def endpoint():
    pickle_file_name = f'endpoint{os.getpid()}.pkl'

    with open(pickle_file_name, 'rb') as data:
        e = pickle.load(data)
        return e


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def metric(request):
    """
    Publish test results to cloudwatch metric named test_success_failure_rate
    """
    # Test finished after yield
    yield

    if request.node.rep_setup.failed:
        logging.info(f'setting up a test failed! : {request.node.nodeid}')
    elif request.node.rep_setup.passed:

        # extract test name from node id
        test_name = request.node.nodeid.split('::')
        metric_name = test_name[len(test_name) - 1]

        if request.node.rep_call.failed:
            logging.info(f'test failed : {request.node.nodeid}')
            metric_value = 0.0
        else:
            logging.info(f'test passed: {request.node.nodeid}')
            metric_value = 1.0

        try:
            response = clients.cloudwatch_client.put_metric_data(
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': 'test_success_failure_rate',
                                'Value': '1.0'
                            },
                        ],
                        'Unit': 'None',
                        'Value': metric_value
                    },
                ],
                Namespace='TestRunner'
            )

            if not response:
                raise Exception(f'Error while performing put metric data operation')

        except Exception as e:
            logging.exception(f'Exception : {e} ')
            return
