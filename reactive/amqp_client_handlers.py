from charms.reactive import when, when_not, set_state
from charmhelpers.fetch import (
    apt_install,
    apt_update,
)
from charmhelpers.core.hookenv import (
    log,
    status_set,
)

PACKAGES = ['python-pika', 'python3-pika']
FILE = '/home/ubuntu/amqp.config'


@when_not('amqp-client.installed')
def install_amqp_client():
    apt_update()
    apt_install(PACKAGES, fatal=True)
    set_state('amqp-client.installed')


@when('amqp.connected')
def setup_amqp_relation(amqp):
    """Use the amqp interface to request access to the amqp broker using our
    local configuration.
    """
    amqp.request_access(username='client',
                        vhost='/')


@when('amqp-client.installed')
@when_not('amqp.available')
def intermediate_status():
    status_set('waiting', 'Client installed. Waiting on amqp relations')


@when('amqp-client.installed')
@when('amqp.available')
def test_amqp(amqp):
    try:
        from charm.amqp_client.client import test
        from pika.exceptions import (
            ProbableAuthenticationError,
            ConnectionClosed,
        )
    except Exception as e:
        msg = "Client failed to import"
        log(msg, "ERROR")
        status_set("blocked", msg)
        raise e
    try:
        # Test last rabbit node added
        if test(amqp.username(), amqp.password(), amqp.rabbitmq_hosts()[-1]):
            msg = "Client Succeded"
            log(msg, "INFO")
            status_set("active", msg)
        else:
            msg = "Client Failed"
            log(msg, "ERROR")
            status_set("blocked", msg)
    except ProbableAuthenticationError as e:
            msg = ("Athentication Failed to {}"
                   "".format(amqp.rabbitmq_hosts()[-1]))
            log(msg, "WARNING")
            status_set("waiting", msg)
    except ConnectionClosed as e:
            msg = ("ConnectionClosed from {}"
                   "".format(amqp.rabbitmq_hosts()[-1]))
            log(msg, "WARNING")
            status_set("waiting", msg)
