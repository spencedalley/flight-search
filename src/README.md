## Setup

Complete the following steps to setup the project: 
1) Install Python3.6 
2) Run `pip install virtualenv`
3) Clone this repository and cd into it. 
4) Run `virtualenv --python=python3.6 .`
5) Run `source bin/activate` to switch to virtualenv interpreter
6) Run `cd src`
7) Run `./manage.py runserver 8000`
8) The server is now up and running with endpoint `/flights/search` ready to be accessed. 

## Main API Logic

The logic for the `flights/search` API is in the `./src/app/views.py` file

## Tests

The tests for this application are in the `./src/app/tests.py` file

## Docker

The Dockerfile and docker-compose.yml file are there, but they aren't complete because I ran out of time to get it working correctly with the searchrunner.scraperapi app. 
