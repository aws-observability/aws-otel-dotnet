AMAZON_TRACE_HEADER_ID = 'X-Amzn-Trace-Id'
LAMBDA_AMAZON_TRACE_HEADER_ID_KEY = 'x-amzn-trace-id'
ROOT = 'root'
RETRIES = 3

# test case constants for extracting values from dict
SEGMENTS = 'Segments'
DOCUMENT = 'Document'
SUBSEGMENTS = 'subsegments'
NAMESPACE = 'namespace'
ID = 'Id'
DURATION = 'Duration'
METADATA = 'metadata'
ANNOTATIONS = 'annotations'

# general test cases paths
HTTP_CALL_PATH = 'outgoing-http-call'
AWS_SDK_CALL_PATH = 'aws-sdk-call'
ANNOTATIONS_METADATA_PATH = 'annotation-metadata'

# python flask web app specific test cases path
FLASK_SQL_ALCHEMY_PATH = 'flask-sql-alchemy-call'
