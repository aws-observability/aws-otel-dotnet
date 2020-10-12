# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from testrunner_tests.utils.utils import invoke_endpoint, get_segment_data_from_response
from testrunner_model.type import Type
from testrunner_tests.utils import constants


# specific test for flask web application
class TestFlaskApp:
    def test_flask_sql_alchemy_call(self, endpoint, metric):
        request_trace_id = invoke_endpoint(Type.WEBAPP.value, f'{endpoint}/{constants.FLASK_SQL_ALCHEMY_PATH}')

        # retrieve traces from x-ray service and load into dictionary
        segment_data, sql_call_trace = get_segment_data_from_response(request_trace_id)

        sql_subsegment_namespace = segment_data[constants.SUBSEGMENTS][0][constants.NAMESPACE]

        for index, _ in enumerate(segment_data[constants.SUBSEGMENTS]):
            assert segment_data[constants.SUBSEGMENTS][index]['sql'] is not None

        assert sql_call_trace[constants.ID] != ''
        assert sql_call_trace[constants.DURATION] != ''
        assert sql_subsegment_namespace == 'remote'
