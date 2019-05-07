from charms import (
    apt
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)

from charms.reactive import (
    when,
    when_not,
    hook,
    set_flag,
    clear_flag,
)

from charmhelpers.core.host import (
    service_restart,
)

from charmhelpers.core.templating import (
    render
)

import os


TEMPLATE_FILE = 'redis-config.tmpl'
CONFIG_FILE = '/etc/newrelic-infra/integrations.d/redis-config.yml'


@when('newrelic-infra.ready')
@when_not('nri-redis.configured')
def configure():
    render(source=TEMPLATE_FILE,
           target=CONFIG_FILE,
           context={
                'hostname': config('hostname'),
                'port': config('port'),
                'keys': config('keys'),
                'keys_limit': config('keys_limit'),
                'password': config('password'),
                'remote_monitoring': True,
                'environment': config('environment'),
            })

    set_flag('nri-redis.configured')

    service_restart('newrelic-infra')
    status_set('active', 'nri-redis ready')


@when('config.changed')
def reconfigure():
    clear_flag('nri-redis.configured')


@when('nri-redis.configured')
def verify_config_exists():
    if not os.path.isfile(CONFIG_FILE):
        clear_flag('nri-redis.configured')


@hook('stop')
def uninstall():
    status_set('maintenance', "Removing nri-redis")

    if os.path.isfile(CONFIG_FILE):
        os.remove(CONFIG_FILE)

    apt.purge(['nri-redis'])
