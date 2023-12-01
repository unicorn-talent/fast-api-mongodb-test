# Web3py, FastAPI and MongoDB

A simple starter for building RESTful APIs with FastAPI and MongoDB.

## Features

- Python FastAPI backend.
- MongoDB database.
- Web3py.
- Deployment.

## Using the applicaiton

To use the application, follow the outlined steps:

1. Clone this repository and create a virtual environment in it:

```console
$ python3 -m venv venv
```

2. Install the modules listed in the `requirements.txt` file:

```console
(venv)$ pip3 install -r requirements.txt
```

3. You also need to start your mongodb instance either locally or on Docker as well as create a `.env` file. See the `.env.sample` for configurations.

   Example for running locally MongoDB at port 27017:

   ```console
   cp .env.sample .env
   ```

4. Start the application:

```console
python main.py
```

The starter listens on port 8000 on address [0.0.0.0](0.0.0.0:8080).

![FastAPI-MongoDB starter](https://user-images.githubusercontent.com/31009679/165318867-4a0504d5-1fd0-4adc-8df9-db2ff3c0c3b9.png)

5. Test the application:

- Set url on browser

## first endpoint

http://localhost:8080/balances/0x7a16ff8270133f063aab6c9977183d9e72835428

## second endpint

http://localhost:8080/info/0x7a16ff8270133f063aab6c9977183d9e72835428

## Deploying the applicaiton using docker

To deploy the application using docker, run following commands:


```console
docker-compose build
docker-compose up
```