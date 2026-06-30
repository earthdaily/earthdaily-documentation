---
title: Account Information
description: Manage your EarthDaily account, API credentials, and orders
keywords:
  - account management
  - API credentials
  - orders
  - EarthDaily Console
  - user account
  - bearer token
---

# Account Information

## Introduction

The Account Information page is the landing page for each user of the customer account when they login to [Account Information](https://console.earthdaily.com/account). It allows the user to check their own account details, orders, and more. It also has links to other applications like EarthPlatform and EarthMosaics.

## Landing Page

Upon logging in, the user arrives at the Landing Page, which shows the applications that the user has access to, and provides links to a rich set of resources:

![Landing Page](../../../assets/platform/AccountUI/AccountLandingPage.png)

On the upper right hand side of the window, you will see the following small icons:

| Icon | Description |
|------|-------------|
| ![About](../../../assets/platform/AccountUI/About.png) | About page that shows the EarthDaily version |
| ![HelpCenter](../../../assets/platform/AccountUI/HelpCenter.png) | Links to report issue, contact us, and learn more |
| ![AppSwitcher](../../../assets/platform/AccountUI/AppSwitcher.png) | Shows a list of hosted applications from EarthDaily; use it to switch between different applications |
| ![UserInfo](../../../assets/platform/AccountUI/UserInfo.png) | Quick information about the signed-in user along with their account and an option to sign out. The user's initials are shown. |

## User Details

From the left menu, the user can access the User Details page.

| S. No | Label | Description |
|-------|-------|-------------|
| ![One](../../../assets/platform/NumberLabels/One.png) | User | Logged in user details |
| ![Two](../../../assets/platform/NumberLabels/Two.png) | Organization | Details of the organization that the user belongs to |
| ![Three](../../../assets/platform/NumberLabels/Three.png) | Credits | [Preview] Shows credits information of the user's organization. Note that this is a Preview feature. |

![Account Information](../../../assets/platform/AccountUI/AccountInformation.png)

## API Credentials

From the left menu, the user can access the API Credentials page.

![Account Information](../../../assets/platform/AccountUI/APICredentials.png)

| S. No | Label | Description |
|-------|-------|-------------|
| ![Four](../../../assets/platform/NumberLabels/Four.png) | API Credentials | Generate "Bearer Token" for API authentication. [Details of How to Provision](../getting-started/authentication.md) |

## My Orders

From the left menu, the user can access the My Orders page. This section allows you to see all the orders placed by the users on the account. You can see the Order details and the order state.

![My Orders](../../../assets/platform/AccountUI/MyOrders.png)

### Order State

| State | Description |
|-------|-------------|
| In Progress | Order is in progress. |
| Error | Order has failed, usually due to a downstream outage. |
| Completed | Order has completed successfully. Ready for download. |
