from testrunner_tests.utils.utils import invoke_endpoint, get_segment_data_from_response
from testrunner_model.type import Type
from testrunner_tests.utils import constants


# general tests for sdk web apps
class TestWebApp:
    def test_aws_sdk_call(self, endpoint, metric):
        # invoke web app endpoint
        request_trace_id = invoke_endpoint(Type.WEBAPP.value, f'{endpoint}/{constants.AWS_SDK_CALL_PATH}')

        # retrieve traces from x-ray service and load into dictionary
        segment_data, aws_sdk_call_trace = get_segment_data_from_response(request_trace_id)

        aws_subsegment_namespace = segment_data[constants.SUBSEGMENTS][0][constants.NAMESPACE]

        for index, _ in enumerate(segment_data[constants.SUBSEGMENTS]):
            assert segment_data[constants.SUBSEGMENTS][index]['aws'] is not None

        assert aws_sdk_call_trace[constants.ID] != ''
        assert aws_sdk_call_trace[constants.DURATION] != ''
        assert aws_subsegment_namespace == 'aws'

    def test_outgoing_http_call(self, endpoint, metric):
        # invoke web app endpoint
        request_trace_id = invoke_endpoint(Type.WEBAPP.value, f'{endpoint}/{constants.HTTP_CALL_PATH}')

        # retrieve traces from x-ray service and load into dictionary
        segment_data, outgoing_http_call_trace = get_segment_data_from_response(request_trace_id)

        http_subsegment_namespace = segment_data[constants.SUBSEGMENTS][0][constants.NAMESPACE]

        for index, _ in enumerate(segment_data[constants.SUBSEGMENTS]):
            assert segment_data[constants.SUBSEGMENTS][index]['http'] is not None

        assert outgoing_http_call_trace[constants.ID] != ''
        assert outgoing_http_call_trace[constants.DURATION] != ''
        assert http_subsegment_namespace == 'remote'

    def test_annotation_metadata(self, endpoint, metric):
        request_trace_id = invoke_endpoint(Type.WEBAPP.value, f'{endpoint}/{constants.ANNOTATIONS_METADATA_PATH}')

        # retrieve traces from x-ray service and load into dictionary
        segment_data, custom_segment_trace = get_segment_data_from_response(request_trace_id)

        assert custom_segment_trace[constants.ID] != ''
        assert custom_segment_trace[constants.DURATION] != ''
        assert segment_data[constants.SUBSEGMENTS][0][constants.METADATA]['default']['integration-test'] == 'true'
        assert segment_data[constants.SUBSEGMENTS][0][constants.ANNOTATIONS]['one'] == '1'
