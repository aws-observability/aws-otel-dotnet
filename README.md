# AWS X-Ray SDK Integration Test Runner

AWS X-Ray SDK Integration Test Runner is an integration testing suite for AWS X-Ray SDK. Test Runner tests AWS X-Ray SDK (provided in different languages) with different frameworks. Currently, Test Runner supports testing X-Ray Python SDK with flask middleware.

## Prerequisites
1. Requires to have web/lambda sample application instrumented with X-Ray SDK
2. Requires web application has all the testing paths that Test Runner supports. Currently Test Runner supports /aws-sdk-call, /outgoing-http-call, /annotations-metadata and /flask-sql-alchemy paths. This means sample flask middleware should support this paths.

## Quick Start
Test Runner can be run with 2 types of application.

```
1. WebApplication
2. LambdaApplication
```

Test Runner by default executes general tests for any language and for any middleware. General tests includes testing aws sdk call instrumentation, http client instrumentation and injection of annotations and metadata. In order to run general tests with any web applications like (springboot, django) make sure web application has /aws-sdk-call, /outgoing-http-call and /annotations-metadata path. Moreover, include only one call per paths e.g. /aws-sdk-call path includes only one call to S3 (ListBuckets). Test Runner can also include framework specific integration tests.

**TestRunner with web app**

Test Runner can be run to test different web frameworks supported by X-Ray SDK. Run Test Runner with Flask web application by executing below command.

```
testrunner.py --t webapp --e http://127.0.0.1:5000 --l python
```
or
```
testrunner.py --type webapp --endpoint http://127.0.0.1:5000 --language python
```

NOTE: Run sample web application before running this module and provide endpoint of the web application as an input here

**TestRunner with lambda app**

Test Runner can be run to test lambda application. Run Test Runner with Lambda application by executing below command.

testrunner.py --t lambda --e lambda-function-name --l python
```
or
```
testrunner.py --type lambda --endpoint lambda-function-name --language python
```
NOTE: Deploy lambda application on AWS Lambda before running this module and provide deployed lambda function name as an input here
