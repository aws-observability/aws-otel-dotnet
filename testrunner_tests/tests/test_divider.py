import os
import pickle
import pytest
import logging

from testrunner_model.type import Type

global_path_dict = {}


def run_tests(app_type, endpoint, sdk_language):
    """
    run tests for either web apps or lambda apps based on app_type
    """
    result = 0
    file_paths = []
    pickle_file_name = f'endpoint{os.getpid()}.pkl'

    # pickle file is used to store endpoint and hook the value into tests
    with open(pickle_file_name, 'wb') as output:
        pickle.dump(endpoint, output, pickle.HIGHEST_PROTOCOL)

    try:
        file_paths.append(f'-v')
        if app_type == Type.WEBAPP.value:
            testfile = os.path.dirname(os.path.realpath(__file__))
            # append general web app tests file path
            file_paths.append(f'{testfile}/web_app/test_web_app_suite.py::TestWebApp')

            # we can add sdk languages and middleware specific conditions to run tests
            if sdk_language.lower() == 'python':
                # append flask web app specific tests file path
                file_paths.append(f'{testfile}/web_app/python/test_flask_app_suite.py::TestFlaskApp')

            result = pytest.main(file_paths)

            del endpoint
            os.remove(pickle_file_name)

            if result != 0:
                exit(1)
            else:
                exit(0)

            return

        elif app_type == Type.LAMBDA.value:
            testfile = os.path.dirname(os.path.realpath(__file__))

            # append general lambda app tests file path
            file_paths.append(f'{testfile}/lambda_app/test_lambda_app_suite.py::TestLambdaApp')

            # run pytest
            result = pytest.main(file_paths)

            del endpoint
            os.remove(pickle_file_name)

            if result != 0:
                exit(1)
            else:
                exit(0)

            return

        else:
            raise Exception(f'lambda and web applications are only supported application types')

    except Exception as e:
        logging.exception(f'Unsupported application type : {e}')
        raise
