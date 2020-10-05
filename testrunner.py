import argparse
import logging
from testrunner_tests.tests import test_divider

# set logging level
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=logging.INFO)


# call test runner function
def run(args):
    test_divider.run_tests(args.test_app_type, args.test_app_endpoint, args.test_sdk_language)


# parse the arguments
def main():
    parser = argparse.ArgumentParser(description='run the test-runner suite')
    parser.add_argument('--type', help='type can be webapp or lambda', dest='test_app_type', type=str, required=True)
    parser.add_argument('--endpoint', help='endpoint can be url for webapp and function name for lambda app',
                        dest='test_app_endpoint', type=str, required=True)
    parser.add_argument('--language', help='AWS X-Ray SDK language to test', dest='test_sdk_language', type=str,
                        required=True)
    parser.add_argument('--h', help='usage of arguments', type=str, required=False)

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
