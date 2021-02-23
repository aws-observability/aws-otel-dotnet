FROM mcr.microsoft.com/dotnet/sdk:3.1 AS build-env
WORKDIR /app
COPY . ./
RUN dotnet add integration-test-app/*.csproj reference opentelemetry-dotnet-contrib/src/OpenTelemetry.Contrib.Extensions.AWSXRay/*.csproj
RUN dotnet add integration-test-app/*.csproj reference opentelemetry-dotnet-contrib/src/OpenTelemetry.Contrib.Instrumentation.AWS/*.csproj
RUN dotnet publish integration-test-app/*.csproj -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:3.1
WORKDIR /app
EXPOSE 8080
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "integration-test-app.dll"]
