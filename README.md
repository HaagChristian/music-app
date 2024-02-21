# fastapi authentication microservice

## Installation

pip install -r requirements.txt

## Description

This API provides endpoints for account registration and user handling.

## Error handling

The errors thrown by the application should not indicate the original problem. Therefore, the errors were intercepted
and replaced by general error messages. This improves security, as it prevents the user from drawing conclusions about
existing data.

## Envs

All required envs are saved in the local.env file