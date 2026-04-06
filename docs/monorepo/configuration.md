---
title: Configuration
description: Configure the EarthOne Python client for different platforms and environments
keywords:
  - configuration
  - environments
  - settings
  - EarthOne client
  - Python SDK
---

# Configuration

The EarthOne Python Client can be configured to operate against
different platforms and environments.

## Environments

The client supports multiple configuration "environments". The primary
environment and the default for using the AWS based Enterprise
Accelerator is `production`, a.k.a.
`AWS_ENVIRONMENT`. The environment selects
not only the client mode (what packages are available in the client) but
also the appropriate URLs used by the client to access the EarthOne
backend services.

There are two mechanisms by which the selection of the environment
described above can be overridden.

If the `EARTHONE_ENV` environment variable is defined when the
`earthdaily.earthone` module (or any submodule) is imported, it will be
used to determine the target environment. It should be set to an
environment name such as `production` as appropriate. This is typically
how one would configure the client when invoked from an execution
environment set up by the user (for example, AWS Lambda or a Kubernetes
workload or other container).

Alternatively, the configuration can be selected at runtime as long as
this is done before importing any of the client modules. For this
purpose, only three submodules are made available to use prior to and
for the purpose of configuring the client: `earthdaily.earthone.auth`,
`earthdaily.earthone.config` and `earthdaily.earthone.exceptions`.
Importing any other submodule of `earthdaily.earthone` will trigger
automatical configuration, and it will then no longer be possible to
configure the client explicitly.

Here is an example of how to configure the client explicitly:

```python
import earthdaily.earthone as eo
eo.select_env(eo.AWS_ENVIRONMENT)

print(f"Using EarthOne environment {eo.get_settings().env}")

# now you can import or access anything else from earthdaily.earthone
eo.catalog.Product.search(...)
```

## Settings

The `Settings` class provides the API for
configuration. The current configuration settings are accessible via the
`get_settings` accesor method.
Among other properties, the following may be most useful to the user:

```python
# the currently configured environment
eo.get_settings().env

# True if in AWS mode:
eo.get_settings().aws_client
```

Please consult the Configuration API documentation for further information.
