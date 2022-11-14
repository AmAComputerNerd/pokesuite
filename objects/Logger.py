from typing import Any
import datetime

class DefaultColour:
    TEXT_INFO = '\033[95m'
    TEXT_HEADER = '\033[94m'
    DEBUG = '\033[96m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    def __init__(self, type : str, default_level : str = 'type-dependant', **kwargs):
        if not (type in ['console', 'file', 'none']):
            raise ValueError(f"Invalid logging type '{type}'")
        self.type = type

        if default_level == 'type-dependant':
            if type == 'console':
                default_level = 'error'
            elif type == 'file':
                default_level = 'debug'
            else:
                default_level = 'none'

        if not (default_level in ['debug', 'info', 'warning', 'error', 'none']):
            raise ValueError(f"Invalid logging level '{default_level}'")
        self.level = default_level

        if self.type in ['file']:
            if kwargs.get('path', None) is not None:
                self.path = str(kwargs['path'])
            raise ValueError(f"Invalid path for logger type: 'file'. Did you forget to provide a path? (e.g. path='./example/example.txt')")

    def get_type(self) -> str:
        '''
        Get the logging type of the Logger.

        Valid types may be:
            - 'console': Log to the console (default). Log level is by default 'error'.
            - 'file': Log to a file. Log level is by default 'debug'.
            - 'none': Do not log. Log level is by default 'none'. This is used mainly for cases where logging is not needed.
        
        Arguments:
            None
        Returns:
            str: The logging type of the Logger.
        '''
        return self.type

    def set_type(self, type : str, **kwargs):
        '''
        Change the logging type of the Logger.

        Valid types may be:
            - 'console': Log to the console (default). Log level is by default 'error'.
            - 'file': Log to a file. Log level is by default 'debug'.
            - 'none': Do not log. Log level is by default 'none'. This is used mainly for cases where logging is not needed.
        
        This method will also change the log level of the Logger to the default log level for the new logging type.
        You can specify a log level to use with the new logging type by passing it as a keyword argument (e.g. `set_type('console', level='debug')`).

        Certain logging types may require additional keyword arguments to be passed to this method.

        Arguments:
            type (str): The new logging type of the Logger.
            **kwargs: Keyword arguments.
        Returns:
            None
        '''
        self.type = type

        if 'level' in kwargs:
            self.level = kwargs['level']
        else:
            if type == 'console':
                self.level = 'error'
            elif type == 'file':
                self.level = 'debug'
            else:
                self.level = 'none'
        
        if self.type in ['file']:
            if kwargs.get('path', None) is not None:
                self.path = kwargs['path']
            raise ValueError(f"Invalid path for logger type: 'file'. Did you forget to provide a path? (e.g. path='./example/example.txt')")

    def get_logging_level(self) -> str:
        '''
        Get the logging level of the Logger.

        Valid logging levels may be:
            - 'debug': Log all messages.
            - 'info': Log all messages except debug messages.
            - 'warning': Log all messages except debug and info messages.
            - 'error': Log all messages except debug, info, and warning messages.
            - 'none': Do not log any messages.
        
        Arguments:
            None
        Returns:
            str: The logging level of the Logger.
        '''
        return self.level

    def set_logging_level(self, level : str):
        '''
        Change the logging level of the Logger.

        Valid logging levels may be:
            - 'debug': Log all messages.
            - 'info': Log all messages except debug messages.
            - 'warning': Log all messages except debug and info messages.
            - 'error': Log all messages except debug, info, and warning messages.
            - 'none': Do not log any messages.
        
        Arguments:
            level (str): The new logging level of the Logger.
        Returns:
            None
        '''
        if not (level in ['debug', 'info', 'warning', 'error', 'none']):
            raise ValueError(f"Invalid logging level '{level}'")
        self.level = level

    def route(self, func, default_output : Any = None, raise_exceptions : bool = False, *args, **kwargs) -> Any:
        '''
        Route a function's output to the Logger.

        The function will be executed and its output will be logged to the Logger.
        Any arguments passed to the function will need to be passed to this method, using either positional or keyword arguments.

        If a function returns normally, the output will be logged as an 'info' message and the function's return value (if any) will be returned.
        If not enough arguments are passed to the function, an error will be logged under the 'warning' log level and no output, or a default value, will be returned.
        If the function raises an exception, the exception will be logged under the 'error' log level, a None or default value will be returned, and the exception will be raised if `raise_exceptions` is True.

        Arguments:
            func (function): The function to route.
            default_output (Any): The default output to return if the function raises an exception or does not return a value.
            raise_exceptions (bool): Whether or not to raise exceptions raised by the function.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        Returns:
            Any: The output of the function, or a default value if the function raises an exception or does not return a value.
        '''
        try:
            output = func(*args, **kwargs)
        except:
            self.error(f"Exception raised when routing function '{func.__name__}' to logger")
            if raise_exceptions:
                raise
            return default_output
        if output is None:
            self.info(f"Function '{func.__name__}' returned None. Default output ({default_output}) will be returned.")
            return default_output
        self.info(f"Function '{func.__name__}' returned {output}")
        return output

    def debug(self, msg : str, force : bool = False):
        '''
        Send a debug message to the Logger.

        Depending on the logging level of the Logger, this message may or may not be logged.
        To force a message to be logged, change the 'force' keyword argument to True.

        Arguments:
            msg (str): The message to log.
            force (bool): Whether or not to force the message to be logged.
        Returns:
            None
        '''
        # Firstly, check the log level to see if the message should be logged.
        if self.__level_check('debug') or force:
            self.__write(f"[{datetime.datetime.now()}] DEBUG ) {msg}", DefaultColour.DEBUG)
        # If the message should not be logged, do nothing.
        return

    def info(self, msg : str, force : bool = False):
        '''
        Send an info message to the Logger.

        Depending on the logging level of the Logger, this message may or may not be logged.
        To force a message to be logged, change the 'force' keyword argument to True.

        Arguments:
            msg (str): The message to log.
            force (bool): Whether or not to force the message to be logged.
        Returns:
            None
        '''
        # Firstly, check the log level to see if the message should be logged.
        if self.__level_check('info') or force:
            self.__write(f"[{datetime.datetime.now()}] INFO  ) {msg}", DefaultColour.INFO)
        # If the message should not be logged, do nothing.
        return

    def warn(self, msg : str, force : bool = False):
        '''
        Send a warning message to the Logger.

        Depending on the logging level of the Logger, this message may or may not be logged.
        To force a message to be logged, change the 'force' keyword argument to True.

        Arguments:
            msg (str): The message to log.
            force (bool): Whether or not to force the message to be logged.
        Returns:
            None
        '''
        # Firstly, check the log level to see if the message should be logged.
        if self.__level_check('warn') or force:
            self.__write(f"[{datetime.datetime.now()}] WARN  ) {msg}", DefaultColour.WARNING)
        # If the message should not be logged, do nothing.
        return
    
    def error(self, msg : str, force : bool = False):
        '''
        Send an error message to the Logger.

        Depending on the logging level of the Logger, this message may or may not be logged.
        To force a message to be logged, change the 'force' keyword argument to True.

        Arguments:
            msg (str): The message to log.
            force (bool): Whether or not to force the message to be logged.
        Returns:
            None
        '''
        # Firstly, check the log level to see if the message should be logged.
        if self.__level_check('error') or force:
            self.__write(f"[{datetime.datetime.now()}] ERROR ) {msg}", DefaultColour.FAIL)
        # If the message should not be logged, do nothing.
        return

    def __write(self, msg : str, colour : str = ""):
        '''
        Internal method for writing to the Logger.

        This method should not be used directly.

        Arguments:
            msg (str): The message to log.
        Returns:
            None
        '''
        if self.type == 'console':
            # Simply print the message to the console.
            print(f"{colour}{msg}{DefaultColour.ENDC}")
        elif self.type == 'file':
            # Open the file and write the message to it. No colouring is done.
            with open(self.path, 'a') as f:
                f.write(f"{msg}")
        # Unimplemented / 'none' type loggers do nothing.
        return

    def __level_check(self, level : str) -> bool:
        '''
        Internal method for checking the log level of the Logger.

        This method should not be used directly.

        Arguments:
            level (str): The log level to check.
        Returns:
            bool: Whether or not a message with the given log level should be logged.
        '''
        if level not in ['none', 'debug', 'info', 'warn', 'error']:
            self.warn(f"Invalid log level: '{level}'")
            return False

        if level == 'none':
            return False
        elif level == 'debug':
            if self.level in ['debug', 'info', 'warn', 'error']:
                return True
        elif level == 'info':
            if self.level in ['info', 'warn', 'error']:
                return True
        elif level == 'warn':
            if self.level in ['warn', 'error']:
                return True
        elif level == 'error':
            if self.level in ['error']:
                return True
        return False

    @staticmethod
    def default_logger():
        '''
        Retrieve the default logger.

        The default logger is a Logger object with the logging type set to 'console' and the log level set to 'error'.

        Arguments:
            None
        Returns:
            Logger: The default logger (console).
        '''
        return Logger("console")

    @staticmethod
    def no_logger():
        '''
        Retrieve a logger that does nothing. This should be used when the logger is not needed, in replacement of None.

        Arguments:
            None
        Returns:
            Logger: A logger that does nothing.
        '''
        return Logger("none")