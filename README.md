# Python Loki server

A way to annoy scrapers with unusable results.

## How to run
There are three ways to run this.

- In your local python
- A self build docker container
- A prebuild docker container

### local python

```shell
$ python http-server.py 
Starting http server
```

### docker container

```shell
$ docker build -t python-loki-server .
$ docker run -p 8080:8080 python-loki-server
```

### Prebuild docker container

```shell
docker pull registry.gitlab.com/aapjeisbaas/python-loki-server:latest
docker run -p 8080:8080 registry.gitlab.com/aapjeisbaas/python-loki-server:latest
```

## What it does

It will return random crap data wrapped in good looking responses like XML SOAP, JSON or HTML.
