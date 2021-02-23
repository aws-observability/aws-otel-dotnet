# AWS Distro for OpenTelemetry .NET SDK

## Introduction

AWS Distro for OpenTelemetry .NET SDK (ADOT .NET SDK) is a distribution of [OpenTelemetry .NET](https://github.com/open-telemetry/opentelemetry-dotnet) SDK, configured to trace applications in a format compatible with the AWS X-Ray service. This way, all the features of the OpenTelemetry project are available, but its components are configured to create traces which can be viewed in the AWS X-Ray console and are configured to allow propagation of those contexts across multiple downstream AWS services.

To send traces to AWS X-Ray, you can use the [AWS Distro for OpenTelemetry (ADOT) Collector](https://github.com/aws-observability/aws-otel-collector). OpenTelemetry .NET SDK exports traces from the application to the ADOT Collector. The ADOT Collector translates OTLE traces to X-Ray compatiable traces and further exports them to X-Ray backend. For more information, read [AWS X-Ray Tracing Exporter for OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/awsxrayexporter).

## Getting Started 

Check out the getting started [documentation](https://aws-otel.github.io/docs/introduction)

## Sample Application

The sample app has included AspNetCore instrumentation, Http instrumentation and OTLP exporter. In addition, it instruments AWS X-Ray id generator in order for the AWS X-Ray back-end to process the traces. It also integrates AWS X-Ray propagator and AWS client instrumentation to trace AWS sdk calls.

See the [example sample application](https://github.com/aws-observability/aws-otel-dotnet/tree/master/integration-test-app) for setup steps.

## Useful Links

* For more information on OpenTelemetry, visit their [website](https://opentelemetry.io/)
* [OpenTelemetry .NET core Repo](https://github.com/open-telemetry/opentelemetry-dotnet)
* [OpenTelemetry .NET Contrib Repo](https://github.com/open-telemetry/opentelemetry-dotnet-contrib)
* [AWS Distro for OpenTelemetry](https://aws-otel.github.io/)
* [AWS Distro for OpenTelemetry Collector](https://github.com/aws-observability/aws-otel-collector)

## License

This project is licensed under the Apache-2.0 License.