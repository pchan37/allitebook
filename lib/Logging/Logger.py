from datetime import datetime

import interrupt

class LoggerConfig(object):

    def __init__(self, include_time):
        """
        Logger configuration class

        An interface to modify the settings of the Logger class; meant only to be
        instantiated inside the Logger class.

        Args:
             include_time (bool): include the time in logs or not

        Returns:
             LoggerConfig: An instance of the class
        """
        self.logging_levels = {'NOT_SET': 0,
                               'DEBUG': 10,
                               'INFO': 20,
                               'WARNING': 30,
                               'ERROR': 40,
                               'CRITICAL': 50}
        self.include_time = include_time

    def overwrite_logging_levels(self, new_logging_levels):
        """
        Overwrites the levels you can log at

        Overwrites the internal dictionary keeping track of the different logging levels
        with the given one.

        Args:
            new_logging_level (dict): new dictionary defining your own set of logging levels

        Returns:
            bool: whether the operation was successful or not
        """
        self.logging_levels = new_logging_levels
        return True

    def set_logging_level(self, logging_level, new_logging_level_value):
        """
        Changes the value of a specific logging level

        Sets the value of the given logging level to the new value

        Args:
            logging_level (str): the name of the logging level you wish to modify the value of
            new_logging_level_value (int): the new value for the logging_level you wish to modify

        Returns:
            bool: whether the operation was successful or not
        """
        if logging_level in self.logging_levels and str(new_logging_level_value).isdigit():
            self.logging_levels[logging_level] = new_logging_level_value
            return True
        else:
            return False

    def add_logging_level(self, logging_level, logging_level_value):
        """
        Adds a new logging level and its corresponding value

        Adds a new logging level along with the priority of the level.  Levels with higher priority
        will be logged more frequently.

        Args:
            logging_level (str): the name of the logging level you wish to add
            logging_level_value (int): the value associated with the new logging level (its priority)

        Returns:
            bool: whether the operation was successful or not
        """
        if logging_level.isalpha() and str(logging_level_value).isdigit():
            self.logging_levels[logging_level] = logging_level_value
            return True
        else:
            return False

    def remove_logging_level(self, logging_level):
        """
        Delete a logging level

        Removes the given logging level from the internal dictionary.  Users may no longer log
        at that level.

        Args:
            logging_level (str): the name of the logging level you wish to delete

        Returns:
            bool: whether the operation was successful or not
        """
        if logging_level in self.logging_levels:
            del self.logging_levels[logging_level]
            return True
        else:
            return False

class Logger:

    def __init__(self, filename, include_time=True):
        """
        A logger class to simplify the logging process

        Abstracts the logging process by opening and writing files behind the scenes and
        logging data if it meets the current logging level.

        Args:
            filename (str): name of the log file
            include_time (bool, optional): include the time in the log file or not

        Returns:
            Logger: an instance of the class
        """
        self.filename = filename
        self.config = LoggerConfig(include_time)
        self.current_logging_level = 'WARNING'

    def set_current_level(self, new_logging_level):
        """
        Changes the current logging level

        Verify that the new logging level is valid and change the current logging level
        to the new logging level.

        Args:
            new_logging_level (str): the name of the new logging level

        Returns:
            bool: whether the operation was successful or not
        """
        if new_logging_level in self.config.logging_levels:
            self.current_logging_level = new_logging_level
            return True
        else:
            return False

    def log(self, message, logging_level=None):
        """
        Log a message

        If the logging_level specified is greater than or equal to the current logging
        level, then log the message into the log.  Include the time if configured to do so.

        Args:
            message (str): the message to enter into the log
            logging_level (str): the level to log the message at

        Returns:
            bool: whether the operation was successful or not
        """

        if logging_level:
            current_logging_value = self.config.logging_levels[self.current_logging_level]
            given_logging_value = self.config.logging_levels[logging_level]

            if given_logging_value >= current_logging_value:
                message = '{0}: {1}'.format(logging_level, message)
            else:
                return None

        if self.config.include_time:
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            message = '{0} {1}'.format(formatted_time, message)

        with interrupt.KeyboardInterruptBlocked():
            with open(self.filename, 'a') as log_file:
                message = '{0}\n'.format(message.strip())
                log_file.write(message)
        return True

    def log_debug(self, message):
        """
        Log a message under the debug level

        If the current logging level is lower than 'DEBUG', log the message.
        Otherwise, return false.

        Args:
            message (str): the message to enter into the log

        Returns:
            bool: whether the operation was successful or not
        """
        return self.log(message, logging_level='DEBUG')

    def log_info(self, message):
        """
        Log a message under the info level

        If the current logging level is lower than 'INFO', log the message.
        Otherwise, return false.

        Args:
            message (str): the message to enter into the log

        Returns:
            bool: whether the operation was successful or not
        """
        return self.log(message, logging_level='INFO')

    def log_warning(self, message):
        """
        Log a message under the warning level

        If the current logging level is lower than 'WARNING', log the message.
        Otherwise, return false.

        Args:
            message (str): the message to enter into the log

        Returns:
            bool: whether the operation was successful or not
        """
        return self.log(message, logging_level='WARNING')

    def log_error(self, message):
        """
        Log a message under the error level

        If the current logging level is lower than 'ERROR', log the message.
        Otherwise, return false.

        Args:
            message (str): the message to enter into the log

        Returns:
            bool: whether the operation was successful or not
        """
        return self.log(message, logging_level='ERROR')

    def log_critical(self, message):
        """
        Log a message under the critcal level

        If the current logging level is lower than 'CRITICAL', log the message.
        Otherwise, return false.

        Args:
            message (str): the message to enter into the log

        Returns:
            bool: whether the operation was successful or not
        """
        return self.log(message, logging_level='CRITICAL')
