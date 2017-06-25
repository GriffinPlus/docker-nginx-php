# Docker Image with NGINX and PHP7-FPM

[![Build Status](https://travis-ci.org/cloudycube/docker-nginx-php7.svg?branch=master)](https://travis-ci.org/cloudycube/docker-nginx-php7) [![Docker 
Pulls](https://img.shields.io/docker/pulls/cloudycube/docker-nginx-php7.svg)](https://hub.docker.com/r/cloudycube/docker-nginx-php7) [![Github 
Stars](https://img.shields.io/github/stars/cloudycube/docker-nginx-php7.svg?label=github%20%E2%98%85)](https://github.com/cloudycube/docker-nginx-php7) [![Github 
Stars](https://img.shields.io/github/contributors/cloudycube/docker-nginx-php7.svg)](https://github.com/cloudycube/docker-nginx-php7) [![Github 
Forks](https://img.shields.io/github/forks/cloudycube/docker-nginx-php7.svg?label=github%20forks)](https://github.com/cloudycube/docker-nginx-php7)

## Overview
This is a Docker image deriving from the [docker-base-supervisor](https://github.com/cloudycube/docker-base-supervisor) image. Summed up  this image is brings along the following features:
- Based on Ubuntu 16.04 LTS
- Support for running multiple services via *supervisord*
- *CloudyCube Container Startup System*
- *NGINX* and *PHP7-FPM* directly from Ubuntu's package repository (no external repositories needed)

The following PHP extensions are included in the image:
- `bcmath`
- `bz2`
- `curl`
- `dba`
- `enchant`
- `fpm`
- `gd`
- `gmp`
- `imap`
- `intl`
- `json`
- `ldap`
- `mbstring`
- `mcrypt`
- `mysql`
- `odbc`
- `opcache` 
- `pgsql`
- `pspell`
- `readline`
- `recode`
- `sqlite3`
- `tidy`
- `xml`
- `xmlrpc`
- `xsl`
- `zip`

This image belongs to a set of Docker images created for project [CloudyCube](http://www.falk-online.eu/projekte/cloudycube). The homepage is in German only, but you will find everything needed to get it working here as well.

## Environment Variables

#### STARTUP_VERBOSITY

The *CloudyCube Container Startup System* (see [base image](https://github.com/cloudycube/docker-base-supervisor) for details) contains a simple logging system with four log levels (error, warning, note, debug) messages can be associated with. The environment variable STARTUP_VERBOSITY determines the maximum log level a message may have to get into the log:

- 0 => Only errors are logged.
- 1 => Errors and warnings are logged.
- 2 => Errors, warnings and notes are logged.
- 3 => All messages are logged.

## For Developers

TBD
