# Docker Image with NGINX and PHP7.2-FPM

[![Build Status](https://travis-ci.com/GriffinPlus/docker-nginx-php7.2.svg?branch=master)](https://travis-ci.com/GriffinPlus/docker-nginx-php7.2)
[![Docker Pulls](https://img.shields.io/docker/pulls/griffinplus/nginx-php7.2.svg)](https://hub.docker.com/r/griffinplus/nginx-php7.2)
[![Github Stars](https://img.shields.io/github/stars/griffinplus/docker-nginx-php7.2.svg?label=github%20%E2%98%85)](https://github.com/griffinplus/docker-nginx-php7.2)
[![Github Stars](https://img.shields.io/github/contributors/griffinplus/docker-nginx-php7.2.svg)](https://github.com/griffinplus/docker-nginx-php7.2)
[![Github Forks](https://img.shields.io/github/forks/griffinplus/docker-nginx-php7.2.svg?label=github%20forks)](https://github.com/griffinplus/docker-nginx-php7.2)

## Overview
This is a Docker image deriving from the [base-supervisor](https://github.com/GriffinPlus/docker-base/tree/master/base-supervisor) image. Summed up this image brings along the following features:
- Based on Ubuntu 18.04 LTS
- Support for running multiple services via *supervisord*
- Griffin+ Container Startup System (see [here](https://github.com/GriffinPlus/docker-base/tree/master/base) for details)
- *NGINX* and *PHP7.2-FPM* directly from Ubuntu's package repository (no external repositories needed)

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

## For Users

### Defining Content to Serve

Any content that is placed below `/var/www/html` is served. There are two ways to let NGINX serve your content. You can either link in a volume containing your content or derive your own image from this image and copy the content into the said directory.

### Environment Variables

#### PHP_FPM_PM

The process manager used by PHP-FPM. The following process managers are supported: `static`, `dynamic` (default) and `ondemand`.

##### static
A fixed number (`PHP_FPM_PM_MAX_CHILDREN`) of child processes is used.
`PHP_FPM_PM_MAX_CHILDREN` defines how many child processes are used.

##### dynamic
The number of child processes is set dynamically based on the following directives.
With this process manager, there will be always at least 1 child.

The following parameters are used:
- `PHP_FPM_PM_MAX_CHILDREN` defines the maximum number of children that can be alive at the same time.
- `PHP_FPM_PM_START_SERVERS` defines the number of children created on startup.
- `PHP_FPM_PM_MIN_SPARE_SERVERS` defines the minimum number of children in 'idle' state (waiting to process). If the number of 'idle' processes is less than this number then some children will be created.
- `PHP_FPM_PM_MAX_SPARE_SERVERS` defines the maximum number of children in 'idle' state (waiting to process). If the number of 'idle' processes is greater than this number then some children will be killed.
  
##### ondemand
No children are created at startup. Children will be forked as needed when new requests are issued.

The following parameters are used:
- `PHP_FPM_PM_MAX_CHILDREN` defines the maximum number of children that can be alive at the same time.
- `PHP_FPM_PM_PROCESS_IDLE_TIMEOUT` defines the number of seconds after which an idle process will be killed.

#### PHP_FPM_PM_MAX_CHILDREN

The number of child processes to be created when `PHP_FPM_PM` is set to `static` and the maximum number of child processes when `PHP_FPM_PM` is set to `dynamic` or `ondemand`. This value sets the limit on the number of simultaneous requests that will be served. The below defaults are based on a server without much resources. Don't forget to tweak the settings to fit your needs.
Used when `PHP_FPM_PM` is set to `static`, `dynamic` or `ondemand`.

Default Value: `5`

#### PHP_FPM_PM_MAX_REQUESTS

The number of requests each child process should execute before respawning. This can be useful to work around memory leaks in 3rd party libraries. For endless request processing specify `0`.

Default Value: `0`

#### PHP_FPM_PM_MAX_SPARE_SERVERS

The desired maximum number of idle server processes. Used only when `PHP_FPM_PM` is set to `dynamic`.

Default Value: `3`

#### PHP_FPM_PM_MIN_SPARE_SERVERS

The desired minimum number of idle server processes. Used only when `PHP_FPM_PM` is set to `dynamic`.

Default Value: `1`

#### PHP_FPM_PM_PROCESS_IDLE_TIMEOUT

The number of seconds after which an idle process will be killed. Used only when `PHP_FPM_PM` is set to `ondemand`.

Default Value: `10s`

#### PHP_FPM_PM_START_SERVERS

The number of child processes created on startup.
Used only when `PHP_FPM_PM` is set to `dynamic`.

Default Value: `PHP_FPM_PM_MIN_SPARE_SERVERS + (PHP_FPM_MAX_PM_SPARE_SERVERS - PHP_FPM_PM_MIN_SPARE_SERVERS) / 2`

#### PHP_INI_DATE_TIMEZONE

The timezone to use in PHP. See [here](http://php.net/manual/en/timezones.php) for possible values.

Default Value: `UTC`

#### PHP_INI_MEMORY_LIMIT

Amount of memory a PHP process may consume. See [here](http://php.net/manual/en/ini.core.php#ini.memory-limit) for details.

Default Value: `32M`

#### STARTUP_VERBOSITY

Determines the verbosity of the *Griffin+ Container Startup System* (see [here](https://github.com/griffinplus/docker-base-supervisor) for details).

- 0 => Logging is disabled.
- 1 => Only errors are logged.
- 2 => Errors and warnings are logged.
- 3 => Errors, warnings and notes are logged.
- 4 => Errors, warnings, notes and infos are logged.
- 5 => All messages (incl. debug) are logged.

Default Value: `4`
