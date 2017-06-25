#!/bin/bash

# This script starts a new instance of the cloudycube/docker-nginx-php7 container and opens a shell in it.
# It is useful in cases where some debugging is needed...

docker run -it \
    --env STARTUP_VERBOSITY=4 \
    cloudycube/docker-nginx-php7 \
    run-and-enter
