---
title: Installation
description: Install the EarthOne Python client library via pip with support for visualization, proxies, and Windows environments
keywords:
  - installation
  - pip install
  - Python client
  - setup
  - proxy configuration
---

# Installation

!!! note
    We strongly suggest to use a virtual environment such as
    `Conda` to work with the EarthOne
    Platform. For more information please see
    [Managing a Development Environment](installation-conda.md).

Install the latest client library via `pip`

```bash
pip install earthdaily-earthone
```

This base version will not include support for interactive features
(maps and graphs in a notebook environment), nor does it include the new
Tables client.

To install with support for the interactive features:

```bash
pip install "earthdaily-earthone[visualization]"
```

The latest development version can always be found on
[GitHub](https://github.com/earthdaily/earthone-python). It can be
installed via `pip`

```bash
pip install -U git+https://github.com/earthdaily/earthone-python.git
```

## Windows Users

The client library requires shapely, which can be hard to install on
Windows with `pip`.

We recommended using [Anaconda](https://conda.io/miniconda.html) to
first install shapely. If you're unfamiliar with `conda`, check out the
document on [development environments](installation-conda.md) for
recommendations.

```bash
conda install shapely
pip install earthdaily-earthone
```

## Using a Firewall Proxy

If your company uses a firewall proxy, you can set environment variables
to point at your company's proxy server:

```bash
$ export HTTP_PROXY="http://10.10.1.10:8080"
$ export HTTPS_PROXY="http://10.10.1.10:8443"

# Setting GRPC is optional, it will fallback to using HTTPS_PROXY
$ export GRPC_PROXY="http://10.10.1.11:8888"
```

Or if you also need to specify a username/password:

```bash
$ export HTTP_PROXY="http://user:pass@10.10.1.10:8080"
$ export HTTPS_PROXY="http://user:pass@10.10.1.10:8443"

# Setting GRPC is optional, it will fallback to using HTTPS_PROXY
$ export GRPC_PROXY="http://user:pass@10.10.1.10:8888"
```

Proxies can also be specified for each protocol using our
ProxyAuthentication class. If a proxy is specified here, it will take
priority over the environment variables
`HTTP_PROXY`,
`HTTPS_PROXY`, and
`GRPC_PROXY`

```python
from earthdaily.earthone.common.http import ProxyAuthentication

# sets the proxy for all protocols
ProxyAuthentication.set_proxy("http://10.10.1.10:8080")

# Or
ProxyAuthentication.set_proxy("http://user:pass@some-proxy:8080", "http")
ProxyAuthentication.set_proxy("http://user:pass@some-proxy:8443", "https")
ProxyAuthentication.set_proxy("http://user:pass@grpc-proxy:8443", "grpc")
```

You can also specify a CA_BUNDLE file:

```bash
$ export REQUESTS_CA_BUNDLE="/path/to/bundle/file"

# (Optional) Set bundle for GRPC. GRPC will fallback to using one of:
#   `SSL_CERT_FILE`
#   `REQUESTS_CA_BUNDLE`
#   `CURL_CA_BUNDLE`
#   Searching system PATH

$ export GRPC_CA_BUNDLE="/path/to/grpc/bundle/file"
```

Also refer to the [requests proxies
documentation](https://requests.readthedocs.io/en/master/user/advanced/#proxies)
and [requests SSL certificate
verification](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification).

## Custom Proxy Authentication

If you need more control and want additional headers, you can register a
instance or subclass of
`ProxyAuthentication`.

```python
from earthdaily.earthone.common.http import ProxyAuthentication

class MyProxyAuth(ProxyAuthentication):
    def authorize(self, proxy, protocol) -> dict:
        # You can do whatever you need to here to generate the approprate headers.

        # Return should be a dictionary with any headers you require.
        # For example
        return {
            "Proxy-Authentication": "Digest some-token",
            "X-Open-Says-Me": "some-super-secret-token",
        }

ProxyAuthentication.register(MyProxyAuth)

# Or you can pass an instance instead
ProxyAuthentication.register(MyProxyAuth())
```

For more information see our API documentation.

## Authentication and Configuration

Once you have installed the EarthOne python client, you will need to
proceed to [authenticate yourself as a user](authentication.md) and
[configure your client](configuration.md).
