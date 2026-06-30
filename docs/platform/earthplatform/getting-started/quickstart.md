---
title: Quick Start
description: Get started quickly with EarthDaily data via API, PySTAC, or Python client
keywords:
  - quick start
  - PySTAC
  - Python client
  - STAC API
  - EarthDaily data
  - authentication
  - satellite data access
---

## Getting Started with EarthDaily STAC APIs

### Table of Contents

- [Authentication](#authentication)
- [EarthDaily Python Client](#earthdaily-python-client)
- [PySTAC](#pystac)

### Authentication

The required `client_id`, `client_secret`, and `access_token_url` values can be found on the [EarthPlatform API Credentials](https://console.earthdaily.com/account/api-credentials) page. **These API credentials are specific to your user account on EarthPlatform and should be kept confidential.**

For more see: [Authentication](authentication.md)


### EarthDaily Python Client

The fastest way to get up and running is to use EarthDaily's [Python SDK](https://github.com/earthdaily/earthdaily-python-client).

First, build a new Virtual Environment and install [`earthdaily`](https://pypi.org/project/earthdaily/):

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the EarthDaily Python client
pip install earthdaily
```

Next, search available collections with the following example:

```python
from dotenv import load_dotenv
from earthdaily import EDSClient, EDSConfig

# Provision EDS.env at https://console.earthdaily.com/account/api-credentials
load_dotenv("EDS.env", override=True) 

client = EDSClient(EDSConfig())

collection_list = list(client.platform.pystac_client.get_all_collections())
collection_list
```


### PySTAC

PySTAC is a library for working with [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org/en) schemas. Please find all the features and capabilities of [PySTAC](https://pystac.readthedocs.io/en/stable/) along with setup details required.

Here is a short snippet showing how to read in credentials set in [Authentication](authentication.md) to query the EarthDaily STAC API using PySTAC:


```python
import os
import requests

from dotenv import load_dotenv
from pystac.client import Client

load_dotenv("EDS.env")  # take environment variables from EDS.env

CLIENT_ID = os.getenv("EDS_CLIENT_ID")
CLIENT_SECRET = os.getenv("EDS_SECRET")
EDS_AUTH_URL = os.getenv("EDS_AUTH_URL")
API_URL = os.getenv("EDS_API_URL")
STAC_API_URL = f"{API_URL}/platform/v1/stac"

session = requests.Session()
session.auth = (CLIENT_ID, CLIENT_SECRET)


def get_new_token(session):
    """Obtain a new authentication token using client credentials."""
    token_req_payload = {"grant_type": "client_credentials"}
    try:
        token_response = session.post(EDS_AUTH_URL, data=token_req_payload)
        token_response.raise_for_status()
        tokens = token_response.json()
        return tokens["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain token: {e}")

token = get_new_token(session)

# Configure pystac client
client = Client.open(STAC_API_URL, headers={"Authorization": f"bearer {token}"})

# Get collections
for collection in client.get_all_collections():
    print(collection)
```
