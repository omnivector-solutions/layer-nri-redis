from pathlib import Path

from charmhelpers.core.hookenv import config
from charmhelpers.core.templating import render

from charms.reactive import (
    when,
    when_not,
    set_flag,
    hook,
    clear_flag,
)

from charms import apt
from charms.layer import status


CONFIG_PATH = Path('/etc/newrelic-infra/integrations.d/redis-config.yml')


@when('newrelic-infra.ready'
      'apt.installed.nri-redis')
@when_not('newrelic-infra.redis.configured')
def configure():
    status.maint('Configuring nri-redis')

    context = {
            'metrics_options': {
                'hostname': config('redis_hostname'),
                'port': config('redis_port'),
                'keys': config('redis_keys'),
                'keys_limit': config('redis_keys_limit'),
                'password': config('redis_password'),
                'remote_monitoring': True,
            },
            # TODO: support for more inventory options
            'inventory_options': {
                'hostname': config('redis_hostname'),
                'port': config('redis_port'),
                'remote_monitoring': True,
            },
            'environment': config('environment'),
    }

    render(source=config('redis-config.yml'),
           target=str(CONFIG_PATH),
           context=context)

    set_flag('newrelic-infra.redis.configured')


@when('config.changed')
def reconfigure():
    clear_flag('newrelic-infra.redis.configured')


@hook('stop')
def uninstall():
    apt.purge(['nri-redis'])
