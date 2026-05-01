---
title: Installing EarthOne
description: How to install and set up your EarthOne Python environment — pip install, authentication, and example notebooks
keywords:
  - EarthOne installation
  - pip install
  - Python client
  - authentication
  - earthone auth login
  - example notebooks
  - Workbench
---

# Installing EarthOne

## How to install and setup your EarthOne Python environment

### Installing the Python Client

> **Note:** If you are using the [Workbench](http://earthone.earthdaily.com/workbench) service, you can skip to [Authentication](https://docs.earthone.earthdaily.com/authentication.html).

To start using the EarthOne Platform, you need to install the Python client. Whether you are using a Virtual Machine (VM) or your local machine, you can install the Python client through [PyPI](https://pypi.org/project/earthdaily-earthone/):

- Take a look at our best practices for [managing your development environment](https://docs.earthone.earthdaily.com/installation-conda.html)
- [Install](https://docs.descarteslabs.com/installation.html) the Python client, typically through `pip install earthdaily-earthone`

### Authenticating your Installation

Once you have installed the EarthOne Python API, we must next [authenticate](https://docs.earthone.earthdaily.com/authentication.html) your Python client with the Platform and test the connection. Typically this is done via a Terminal in an activated environment, such as [Conda](https://conda.io/projects/conda/en/latest/index.html), with the following command:

```
earthone auth login
```

> **Note:** If you run into trouble with authentication, please feel free to reach out to [dl.support@earthdaily.com](mailto:dl.support@earthdaily.com).

### Example Notebooks to get you started

The notebooks are located in our Jupyter Lab environment [Workbench](https://earthone.earthdaily.com/workbench). Alternatively, you can visit our [GitHub repository](https://github.com/earthdaily/earthone-example-notebooks/) to learn how to use the Platform. The repository covers everything from basic concepts and API usage to creating a simple web application that takes advantage of Platform services. To get started, simply clone the repository to your local machine and explore the Jupyter notebooks in the `guides/` folder.

```
git clone https://github.com/earthdaily/earthone-example-notebooks.git
```

Sample notebooks include examples of working with the API, including modeling, feature annotation, and real-time pipeline orchestration. See the [GitHub repo](https://github.com/earthdaily/earthone-example-notebooks/) for more information.
