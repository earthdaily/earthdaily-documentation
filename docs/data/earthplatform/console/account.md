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

## General Information

On the upper right hand side of the window, you will see three small icons:

| Icon | Description |
|------|-------------|
| ![About](../../../assets/data/AccountUI/About.png) | About page that shows the EarthDaily version |
| ![AppSwitcher](../../../assets/data/AccountUI/AppSwitcher.png) | Shows a list of hosted applications from EarthDaily; use it to switch between different applications |
| ![UserInfo](../../../assets/data/AccountUI/UserInfo.png) | Quick information about the signed-in user along with their account and an option to sign out |

## My Account

| S. No | Label | Description |
|-------|-------|-------------|
| ![One](../../../assets/data/NumberLabels/One.png) | User | Logged in user details |
| ![Two](../../../assets/data/NumberLabels/Two.png) | Account | Details of the account that the user belongs to |
| ![Three](../../../assets/data/NumberLabels/Three.png) | API Credentials | Token URL to generate "Bearer Token" for API authentication. [Details of How to Provision](../getting-started/authentication.md) |
| ![Four](../../../assets/data/NumberLabels/Four.png) | Hosted Apps | Use this to switch between various apps available |

![Account Information](../../../assets/data/AccountUI/AccountInformation.png)

## My Orders

My Orders section allows you to see all the orders placed by the users on the account. You can see the Order details and the order state.

![My Orders](../../../assets/data/AccountUI/MyOrders.png)

## Order State

| State | Description |
|-------|-------------|
| Pending | Order is being validated and will be accepted for processing once validation passes |
| Accepted | Order has been accepted and will be processed |
| Failed | Order has failed, usually due to a downstream outage. You may retry. |
| Succeeded | Order has completed successfully. Ready for download. |
