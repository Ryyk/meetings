# REST API With Flask, SQL Alchemy

[![Build Status](https://travis-ci.com/Ryyk/meetings.svg?token=8YLktDDQipLLgFGN1NpP&branch=master!)](https://travis-ci.com/Ryyk/meetings)

> Meetings API using Python Flask, SQL Alchemy and Marshmallow

## Requirements

This tutorial utilizes the following software:

1. Python v3.7.3
1. Postman (Design and Test APIs)

## Project Setup

1. Create a new directory to store the project:

    ```sh
    $ mkdir meetings
    $ cd meetings
    ```

1. Create and activate your virtual env and install requirements.txt:

    ```sh
    $ virtualenv venv
    $ venv\Scripts\activate
    $ (env)$ pip install -r requirements.txt
    ```

2. Run server (http://localhost:5000):

    ```sh
    (env)$ python app/app.py
    ```

3. Run tests:

    ```sh
    (env)$ python app/app_test.py
    ```
## Assumptions:

> Some assumptions were made when creating the data model:

* Multiple records of the same meeting are allowed
* The host is a Viewer
* The viewers email is unique


## Endpoints

- **POST**    /meeting/create - **Create a Meeting**
> { "host_email": string,  "password": string }
- **GET**     /meeting/get - **Get All Meetings**
- **GET**     /meeting/get/:id - **Get Single Meeting**
- **POST**    /recording/create - **Create a Recording**
> { "url": string,  "is_private": bool, "meeting_id": int }
- **DELETE**  /recording/delete - **Delete Recording**
> { "url": string }
- **POST**    /recording/share - **Share Recording**
> { "url": string,  "email": string }
- **GET**     /recording/has-access - **Verify if a Viewer has access to a specific Recording**
> { "url": string,  "email": string }
- **GET**     /recording/get - **Get All Recordings**
- **GET**     /recording/get/:url - **Get Single Recordings**
- **POST**    /viewer/create - **Create a Viewer**
> { "email": string }
- **GET**     /viewer/get - **Get All Viewers**

> **NOTE**: Some requests require a json with additional information. 

## Notes

1. **Why Marshmallow**:
marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes. Marshmallow schemas can be used to:
   - Validate input data.
   - Deserialize input data to app-level objects.
   - Serialize app-level objects to primitive Python types. The serialized objects can then be rendered to standard formats such as JSON for use in an HTTP API.

1. **Using Postman to test the APIs**:
Postman is a great tool when trying to test RESTful APIs. It offers a sleek user interface with which to make HTML requests, without the hassle of writing a bunch of code just to test an API's functionality.



