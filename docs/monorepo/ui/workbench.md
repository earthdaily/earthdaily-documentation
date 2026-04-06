---
title: Workbench
description: Hosted JupyterLab environment with pre-configured integrations for the EarthOne Platform APIs
keywords:
  - Workbench
  - JupyterLab
  - notebook environment
  - cloud IDE
  - development environment
---

# Workbench

Workbench is a hosted JupyterLab environment that combines a ready-to-go
environment with custom integrations to the EarthOne Platform APIs.

## Starting a Server

When you log in to <https://earthone.earthdaily.com/workbench> for the
first time, you'll be presented with the hub home, where you can choose
to start (and later stop or connect to) your jupyterlab server. Clicking
the `Start My Server` button presents you with a choice of the type of
compute instance you would like to use -- either a Model
exploration/Development or a Model Training instance. Choose the
environment that is best suited for your work. You can always stop and
start a different type of server if you decide to change. Your home
directory will persist across instance types.

## Getting Started

To get started you will need to go through a one-time initialization of
your environment in order to set up the proper authentication token for
future API calls with the Python client library.

A notebook named `"01 Logging In.ipynb"` is located in the
`"example-notebooks/"` directory in your filesystem browser. Open the
notebook and follow the instructions to add your credentials to the home
directory of your JupyterLab environment. Alternatively, you can open a
terminal in JupyterLab, execute the command `earthone auth login`, and
follow the instructions listed there.

## Pre-loaded Examples

Upon server startup, a set of examples are copied to the
`example-notebooks` folder in your home directory. These examples are a
good starting point for exploring and understanding how you can use the
EarthOne Platform APIs and visualization tools. These examples are
refreshed at server start time, and will overwrite contents in the
`example-notebooks` directory. Avoid saving work to that directory.

## Server Lifecycle

Your JupyterLab server will occasionally be shut down if it is deemed
inactive (based on interactions with the JupyterLab interface). To
restart, simply go through the same steps to start a server. You will
not need to re-initialize your environment. To manually shut down a
server, navigate to the hub home at
<https://earthone.earthdaily.com/workbench/hub/home> and click the
`Stop My Server` button. After a few seconds the server will shut down,
at which point you could either log out or start a server of a different
type, depending on what you intend to do next.

### Data Persistence

All data in your `${HOME}` (`/home/jovyan`) directory is persisted
across servers. Any modifications to the rest of the system will lost at
server shutdown/restart. Example notebooks are loaded at server start
time, and will overwrite contents in the `example-notebooks` directory.
Avoid saving work to that directory.
