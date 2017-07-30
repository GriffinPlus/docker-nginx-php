"""
This module contains everything needed to configure 'php7-fpm'.
Author: Sascha Falk <sascha@falk-online.eu>
License: MIT License
"""

import os
import re

from configparser import ConfigParser
from ..cc_helpers import read_text_file, write_text_file, replace_php_define, replace_php_variable, generate_password, get_env_setting_bool, get_env_setting_integer, get_env_setting_string
from ..cc_log import Log
from ..cc_service import Service


# ---------------------------------------------------------------------------------------------------------------------


CONFIGURATION_FILE_PATH = '/etc/php/7.0/fpm/pool.d/www.conf'


# ---------------------------------------------------------------------------------------------------------------------


# name of the service
service_name = 'php7-fpm'

# determines whether the service is run by the startup script
enabled = True

def get_service():
    "Returns an instance of the service provided by the service plugin."
    return PHP7_FPM()


# ---------------------------------------------------------------------------------------------------------------------


#                                       setting name                type   min   max
PHP_FPM_SETTINGS = {
    'PHP_FPM_PM'                      : ('pm',                      'str'             ),
    'PHP_FPM_PM_START_SERVERS'        : ('pm.start_servers',        'int', 1,    None ),
    'PHP_FPM_PM_MIN_SPARE_SERVERS'    : ('pm.min_spare_servers',    'int', 1,    None ),
    'PHP_FPM_PM_MAX_SPARE_SERVERS'    : ('pm.max_spare_servers',    'int', 1,    None ),
    'PHP_FPM_PM_MAX_CHILDREN'         : ('pm.max_children',         'int', 1,    None ),
    'PHP_FPM_PM_PROCESS_IDLE_TIMEOUT' : ('pm.process_idle_timeout', 'int', 1,    None ),
    'PHP_FPM_PM_MAX_REQUESTS'         : ('pm.max_requests',         'int', 1,    None ),
}


#                                        setting name               type   min   max   force
PHP_INI_SETTINGS = {
    'PHP_INI_MEMORY_LIMIT'            : ('memory_limit',            'str', None, None, True),
    'PHP_INI_DATE_TIMEZONE'           : ('date.timezone',           'str', None, None, False),
}


# ---------------------------------------------------------------------------------------------------------------------


class PHP7_FPM(Service):

    def prepare(self):
        """
        Reads environment variables and checks preconditions the following call to configure() needs to succeed. In case
        of anything being screwed in the configuration or system, this method should throw an exception to abort starting
        up before configure() modifies any configuration files.
        """

        # load configuration file
        # ---------------------------------------------------------------------------------------
        if os.path.exists(CONFIGURATION_FILE_PATH):
            self._config = ConfigParser()
            self._config.read(CONFIGURATION_FILE_PATH, encoding='utf-8')
        else:
           raise RuntimeError('The configuraton file ({0}) does not exist.'.format(CONFIGURATION_FILE_PATH))

        # the entire configuration is in section 'www'
        # ---------------------------------------------------------------------------------------

        section = self._config['www']

        # PHP-FPM settings
        # ---------------------------------------------------------------------------------------

        for (key, info) in sorted(PHP_FPM_SETTINGS.items(), key=lambda x: (x[0])):

            value = None

            if info[1] == 'bool':
                value = get_env_setting_bool(key, None)
                if value == True: value = 'on'
                if value == False: value = 'off'
            elif info[1] == 'int':
                value = get_env_setting_integer(key, None, info[2], info[3])
                if value: value = str(value)
            elif info[1] == 'str':
                value = get_env_setting_string(key, None)
            else:
                raise RuntimeError('Invalid variable type ({0}).'.format(value[1]))

            if value:
                section[info[0]] = value

        # PHP-FPM settings
        # ---------------------------------------------------------------------------------------

        for (key, info) in sorted(PHP_INI_SETTINGS.items(), key=lambda x: (x[0])):

            value = None

            if info[1] == 'bool':
                value = get_env_setting_bool(key, None)
                if value:
                    if info[4]:
                        value = 'on' if value else 'off'
                        section['php_admin_flag[{0}]'.format(info[0])] = value
                    else:
                        section['php_flag[{0}]'.format(info[0])] = value
            elif info[1] == 'int':
                value = get_env_setting_integer(key, None, info[2], info[3])
                if value:
                    if info[4]: section['php_admin_value[{0}]'.format(info[0])] = str(value)
                    else:       section['php_value[{0}]'.format(info[0])]       = str(value)
            elif info[1] == 'str':
                value = get_env_setting_string(key, None)
                if value:
                    if info[4]: section['php_admin_value[{0}]'.format(info[0])] = value
                    else:       section['php_value[{0}]'.format(info[0])]       = value
            else:
                raise RuntimeError('Invalid variable type ({0}).'.format(value[1]))



    # ---------------------------------------------------------------------------------------------------------------------


    def configure(self):
        """
        Creates/modifies the configuration file according to environment variables.
        """

        # write configuraton file
        with open(CONFIGURATION_FILE_PATH, 'w') as configfile:
            self._config.write(configfile)

    # ---------------------------------------------------------------------------------------------------------------------


