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

1. Run the server:

    ```sh
    (env)$ python app/app.py
    ```

1. Run the tests:

    ```sh
    (env)$ python app/app_test.py
    ```
## Assumptions:

> Some assumptions were made when creating the data model:

* Multiple records of the same meeting are allowed
* The host is a Viewer
* The viewers email is unique


## Endpoints

* POST    /meeting/create
* GET     /meeting/get
* GET     /meeting/get/:id
* POST    /recording/create
* DELETE  /recording/delete
* POST    /recording/share
* GET     /recording/has-access 
* GET     /recording/get
* GET     /recording/get/:url
* POST    /viewer/create
* GET     /viewer/get

## Endpoints Reasoning

* /meeting/create
* /meeting/get
* /meeting/get/:id
* /product/:id
* /product/:id

## Notes

1. Why Marshmallow:
> json

2. Using Postman to test de API:


