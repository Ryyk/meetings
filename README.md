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
    (env)$ python  app/app_test.py
    ```

## Endpoints

* GET     /product
* GET     /product/:id
* POST    /product
* PUT     /product/:id
* DELETE  /product/:id
