#!/bin/bash

# This script starts a new instance of the griffinplus/nginx-php7 container and opens a shell in it.
# It is useful in cases where some debugging is needed...

docker run -it \
    --env STARTUP_VERBOSITY=4 \
    --env PHP_FPM_PM=ondemand \
    --env PHP_FPM_PM_MAX_CHILDREN=10 \
    --env PHP_FPM_PM_MAX_REQUESTS=1000 \
    --env PHP_FPM_PM_MAX_SPARE_SERVERS=20 \
    --env PHP_FPM_PM_MIN_SPARE_SERVERS=10 \
    --env PHP_FPM_PM_PROCESS_IDLE_TIMEOUT=300 \
    --env PHP_FPM_PM_START_SERVERS=5 \
    --env PHP_INI_DATE_TIMEZONE=UTC \
    --env PHP_INI_MEMORY_LIMIT=128M \
    griffinplus/nginx-php7.2 \
    run-and-enter
