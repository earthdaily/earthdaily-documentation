---
title: Authentication
description: Set up authentication credentials for the EarthOne Platform using CLI or environment variables
keywords:
  - authentication
  - credentials
  - API keys
  - login
  - EarthOne CLI
---

# Authentication

Before you can begin using the services provided by the platform, you
need to set up authentication credentials. The easiest way is to use the
CLI helper.

```bash
earthone auth login
```

For non-interactive environments, one needs to set the
EARTHONE_CLIENT_ID and EARTHONE_CLIENT_SECRET (or
EARTHONE_REFRESH_TOKEN) environment variables. These can be retrieved
using the CLI helper after completing the login process or generated
fresh through [IAM](https://earthone.earthdaily.com/account/api-keys).

If you want to retrieve the client id and client secret using the CLI
helper, you can use the following.

```bash
earthone auth env
```

Then you can define them as environment variables in the non-interactive
environment where you run your code using the EarthOne client. Do be
aware that these credentials are sensitive and anyone who has access to
them gains access to your EarthOne resources.

```bash
export EARTHONE_CLIENT_ID=...
export EARTHONE_CLIENT_SECRET=...
```

You can test the authentication credentials with the following.

```bash
earthone auth env
earthone auth groups
```

See the authentication client `Auth` for
additional information and options.

## Common Authentication Issues

In general, the logic will either retrieve the cached credentials from
`~/.earthone/token_info.json` or use credentials encoded in environment
variables. The logic will never mix and match; the credentials encoded
in environment variables take precedent over the cached credentials.

There are sometimes scenarios where you receive an unexpected error
message.

------------------------------------------------------------------------

```bash
AuthError: No valid authentication info found (no client_id). See https://earthone.earthdaily.com/docs/authentication.html.
```

This means that one or more pieces of information are missing. The text
between the parenthesis in the error message will give you a hint as to
what might be missing.

The `no client id` means that there is no authentication information at
all either cached or in the environment, or you have set the
`EARTHONE_CLIENT_SECRET` but not the corresponding `EARTHONE_CLIENT_ID`.
If you use the cached information, make sure you ran
`earthone auth login` successfully, and once that has completed that the
file `~/.earthone/token_info.json` is present, readable and writable
only by you, and contains valid information. If you're using environment
variables, make sure you have exported them both in your shell.

The `no client_secret or refresh_token` means that you have set the
`EARTHONE_CLIENT_ID` but not the corresponding `EARTHONE_CLIENT_SECRET`.

------------------------------------------------------------------------

```bash
OauthError: Could not retrieve token: {"error":400,"message":"invalid grant_type"}
```

This means that the authentication information is invalid. This is less
likely the case with cached information, and more likely if you use
environment variables.

If you copy and paste one or both values, make sure you remove the
quotes or make sure they're ASCII quotes. Oftentimes, copying the values
including the quotes from other documents will introduce non-ASCII
quotes which will cause this error message.

As a last resort, verify that values are complete and correct. Missing a
single character will cause this error message.

------------------------------------------------------------------------

```bash
OauthError: Could not retrieve token: {"error":"invalid_refresh_token","error_description":"specified refresh_token does not exist","statusCode":401}
```

This means that you revoked the secret that you're using. You can list
the secrets you have created using the page
<https://earthone.earthdaily.com/account/api-keys>. You can revoke any
of your secrets as needed if you think a secret has been compromised or
otherwise is not needed any more.
