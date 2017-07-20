import interrupt

class Config(object):

    def __init__(self, filename):
        """
        A config class to simplify the usage of a config file

        Abstracts the process of storing data in a configuration file removing the need
        to parse the configuration file yourself.  If the file already exists, parse it
        as a configuration file.  Otherwise, create a configuration file with that name
        and store the config data in it.

        Args:
            filename (str): name of the configuration file

        Returns:
            Config: an instance of the class
        """
        self.filename = filename
        self.config = self._read_config() or {}

    def _read_config(self):
        """
        Read and parses the configuration file

        Open the file specified to the constructor and parses the content to fill
        a dictionary.  Return None if the file does not exists or is corrupted.

        Args:

        Returns:
            dict: a dictionary with the config data if file exists and is not corrupted
            None: if the file was corrupted or does not exists
        """
        try:
            config = {}
            with open(self.filename) as config_file_handler:
                config_file_content = config_file_handler.readlines()
            for line in config_file_content:
                line_without_newline = line.strip('\n')
                key, value = line_without_newline.split('=', 1)
                config[key] = int(value) if value.isdigit() else value
            return config
        except IOError:
            return None

    def set_default_value(self, key, value):
        """
        Set the value of the key to the specified value if the value is not set

        Create a new key-value in the config dictionary if the key does not exist.
        Otherwise, do nothing.

        Args:
            key (str): the name of the key-value pair
            value (str): the value associated with the key

        Returns:
            bool: if the value was changed or not
        """
        if not key in self.config:
            self.set(key, value)

    def set(self, key, value):
        """
        Set the value of the key to the specified value

        Create a new key-value in the config dictionary if the key does not exist.
        Otherwise, set the current value of the key to the specified value.

        Args:
            key (str): the name of the key-value pair
            value (str): the value associated with the key

        Returns:
            None: if the key-value pair did not previously exists
            str: the previous value if the key-value pair already exists
        """
        previous_value = self.get(key)
        self.config[key] = value
        return previous_value

    def get(self, key):
        """
        Get the value of the specified key

        Retrieve the current value of the specified key if the key exists and return
        None if the key does not.

        Args:
            key (str): the name of the key-value pair

        Returns:
            None: if the key-value pair does not exists
            str: the current value of the specified key
        """
        return self.config.get(key)

    def save(self):
        """
        Save the config data

        Overwrite or create a new file and write the configuration data in the following
        format, key: value

        Args:

        Returns:
            bool: if the operation was successful or not
            OSError (optional): the os error message if the operation was not successful
        """
        try:
            with interrupt.KeyboardInterruptBlocked():
                config_file_content = []
                for key, value in sorted(self.config.items()):
                        line = '{0}={1}\n'.format(key, value)
                        config_file_content.append(line)
                with open(self.filename, 'w') as config_file_handler:
                    config_file_handler.writelines(config_file_content)
            return True
        except OSError as os_error:
            return False, os_error
