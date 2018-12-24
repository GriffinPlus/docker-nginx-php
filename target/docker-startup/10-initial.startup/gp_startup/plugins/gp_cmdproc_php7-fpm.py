"""
This module contains everything needed to configure 'php7-fpm'.
Author: Sascha Falk <sascha@falk-online.eu>
License: MIT License
"""

import os
import re

from configparser import ConfigParser

from ..gp_log import Log
from ..gp_cmdproc import CommandProcessor, PositionalArgument, NamedArgument
from ..gp_errors import GeneralError, CommandLineArgumentError, FileNotFoundError, IoError, EXIT_CODE_SUCCESS
from ..gp_helpers import read_text_file, write_text_file, replace_php_define, replace_php_variable, generate_password, get_env_setting_bool, get_env_setting_integer, get_env_setting_string


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


CONFIGURATION_FILE_PATH = '/etc/php/7.2/fpm/pool.d/www.conf'

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


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


# name of the processor
processor_name = 'php7-fpm'

# determines whether the processor is run by the startup script
enabled = True

def get_processor():
    "Returns an instance of the processor provided by the command processor plugin."
    return PHP7_FPM()


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


class PHP7_FPM(CommandProcessor):

    # -------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        # let base class perform its initialization
        super().__init__()

        # register command handlers
        self.add_handler(self.run, PositionalArgument("run"))
        self.add_handler(self.run, PositionalArgument("run-and-enter"))


    # -------------------------------------------------------------------------------------------------------------------------------------


    def run(self, pos_args, named_args):

        # load configuration file
        # ---------------------------------------------------------------------------------------
        if os.path.exists(CONFIGURATION_FILE_PATH):
            config = ConfigParser()
            config.read(CONFIGURATION_FILE_PATH, encoding='utf-8')
        else:
           raise FileNotFoundError('The configuraton file ({0}) does not exist.'.format(CONFIGURATION_FILE_PATH))

        # the entire configuration is in section 'www'
        # ---------------------------------------------------------------------------------------

        section = config['www']

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

        # write configuraton file
        # ---------------------------------------------------------------------------------------
        with open(CONFIGURATION_FILE_PATH, 'w') as configfile:
            config.write(configfile)


        return EXIT_CODE_SUCCESS

    # -------------------------------------------------------------------------------------------------------------------------------------

