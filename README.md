# collectd-tls-expiry-monitoring

[![Build Status](https://travis-ci.org/stefan2904/collectd-tls-expiry-monitor.svg?branch=master)](https://travis-ci.org/stefan2904/collectd-tls-expiry-monitor)

Minimal collectd module to report expiry time of a HTTPS TLS certificate.


## Usage

See `collectd.conf` for an example (minimal) config.


## Example

```
<Plugin python>
    ModulePath "/path/to/modules/"
    Import "tls_cert_monitor"
    <Module tls_cert_monitor>
        hosts "github.com" "google.com"
    </Module>
</Plugin>
```

```
demoserver1.tls-cert-monitor.gauge-github_com 7848249 1518710150
demoserver1.tls-cert-monitor.gauge-google_com 5848449 1518710151
```

Test config using `collectd -T -C collectd.conf`.


## Resources

* https://collectd.org/documentation/manpages/collectd-python.5.shtml
* https://collectd.org/documentation/manpages/collectd-python.5.shtml#dispatch
* https://serverlesscode.com/post/ssl-expiration-alerts-with-lambda/
