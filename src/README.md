# newrelic-infra layer

This layer Installs and configures the newrelic-infra agent with the nri-redis package

## Usage
  ```
    juju deploy cs:~rr-pdl/nri-redis
    juju config nri-redis license_key=<newrelic_key>
    juju relate nri-redis <application>
  ```
