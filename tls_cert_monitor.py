import datetime
import socket
import collectd
import ssl

PLUGIN_NAME = 'tls-cert-monitor'
INTERVAL = 60  # seconds

_hosts = None

collectd.info('tls-cert-monitor: Loading Python plugin: ' + PLUGIN_NAME)


def configure(configobj):
    '''Configure this plugin based on collectd.conf parts.

    Example configuration:

    LoadPlugin python
    ...
    <Plugin python>
        ModulePath "/usr/local/lib/collectd/python/"
        LogTraces true
        Interactive false
        Import "tls_cert_monitor"
        <Module tls_cert_monitor>
            hosts "github.com" "google.com"
        </Module>
    </Plugin>
    '''

    global _hosts

    collectd.info(
        'tls-cert-monitor: Configure with: key=%s, children=%r' %
        (configobj.key, configobj.children))

    config = {c.key: c.values for c in configobj.children}
    collectd.info('tls-cert-monitor: Configured with %r' % (config))

    # Set a module-global based on external configuration
    _hosts = config.get('hosts')
    # _domains = next(iter(config.get('hosts')))


def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.utcnow()


def read(data=None):
    for host in _hosts:
        r = ssl_valid_time_remaining(host)
        r = r.total_seconds()
        r = int(r)

        collectd.info(
            'tls-cert-monitor(host=%s): Reading data (data=%d)' %
            (host, r))

        val = collectd.Values(type='gauge', type_instance=host)
        val.plugin = 'tls-cert-monitor'
        val.dispatch(values=[r])


collectd.register_config(configure)
collectd.register_read(read, INTERVAL)
