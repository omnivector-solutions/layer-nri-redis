# nri-redis

This charm Installs and configures the newrelic-infra agent with the
nri-redis host integration.


## Usage
To deploy this charm, configure the `license_key` and relate to an application exposing
the `juju-info` provides endpoint.

```bash
juju deploy cs:~omnivector/nri-redis --config license_key=<newrelic_key>
juju relate nri-redis <application>
```

This charm will set a blocked status in the case the `license_key` is not set.

To configure the `license_key` following deployment use `juju config`.
```bash
juju config nri-redis license_key=<newrelic_key>
```

To remove the `newrelic-infra` agent, simply remove the application or unit.


#### License
* AGPLv3 (see `LICENSE` file in this directory).
