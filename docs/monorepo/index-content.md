---
title: EarthOne Platform Overview
description: Introduction to the EarthOne Platform for global-scale geospatial raster data analysis with Python
keywords:
  - EarthOne Platform
  - geospatial data
  - Python client
  - satellite imagery
  - raster data
---

# EarthOne Platform

The EarthOne Platform simplifies analysis of **global-scale raster
data** by providing:

- Access to a catalog of petabytes of disparate geospatial data, all normalized and interoperable through one [common interface](guides/catalog.md)
- A [Python client library](api.md) to access these systems

## Create an Account

This is a publicly installable package. However, if you want access to
our full Platform and data catalog, you will need to create a EarthOne
account and request access:

- Sign up at <https://earthone.earthdaily.com/>
- Send an email to your contact at EarthOne or visit our [support portal](https://earthone.earthdaily.com/support) to request access

## Install the Python Client

If you plan to interact with the Platform programmatically, you should
install the Python client and run a quick test to make sure everything’s
working.

- Take a look at our best practices for [managing your development environment](installation-conda.md)
- [Install](installation.md) the Python client
- [Authenticate](authentication.md) with the Platform and test the connection
- [Familiarize yourself](introductory-example.md) with our Python client

!!! note
    At a minimum, we support the three most recent minor versions of the
    client. Each minor version is supported for up to a year, with the
    exception that support for all versions prior to 5.0 will be dropped
    on Dec 1, 2025 and these versions will no longer function after that
    time.
    
    Currently the supported releases are:
    
    - `6.0` (Feb 17, 2026)
    - `5.0` (Aug 20, 2025)
    
    We only support the latest patch release (e.g. `6.0.X`) for any minor
    version.
    
    We recommend that all users upgrade to version `6.0` as soon as
    possible. It contains many bug fixes and performance improvements, and
    is the only version that will receive new features and bug fixes going
    forward.

## How to Use These Docs

Our docs are broken up into several sections, in increasing level of
detail:

- **Examples** demonstrate smaller pieces of
  functionality and are geared toward composability. We’re always adding
  to these examples, so let us know if there’s a topic you would like to
  see.
- [Guides](guide.md) contain best practices and contain more context than
  Examples.
- Our [API reference](api.md) is there when you need to dig in to usage
  subtleties.

## Support

Feel free to contact our Support Team at any time through our [support
portal](https://earthone.earthdaily.com/support)

## Status Page

If you are having intermittent issues with software functionality, check
the [Platform Status Page](https://earthone.earthdaily.com/status) for
the real-time status of known issues impacting Platform performance.
