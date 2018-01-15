import signal

class KeyboardInterruptBlocked(object):

    def __init__(self, ProgressBarObject=None):
        '''
        Blocks the KeyboradInterrupt signal

        Temporarily block the KeyboardInterrupt signal, restore the handler for SIGINT,
        and raise KeyboardInterrupt if necessary.

        Args:

        Returns:
            KeyboardInterruptBlocked: An instance of the class
        '''
        self.ProgressBar = ProgressBarObject

    def __enter__(self):
        '''
        Mute the KeyboardInterrupt signal

        Store the default handler for SIGINT (KeyboardInterrupt), replace the handler
        with our own to ignore KeyboardInterrupt signal.

        Args:

        Returns:

        '''
        self.received_signal = False
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, signum, frame):
        '''
        Handle the SIGINT signal

        Update the message for the progress bar object if there is one and store the
        components of the triggered signal so that the signal can be raised later.

        Args:
            signum (int) : the number associated with the triggered signal
            frame (str): the stack frame when the signal was triggered

        Returns:

        '''
        if self.ProgressBar:
            self.ProgressBar.set_message('Finishing up...')
        self.received_signal = (signum, frame)

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        Unmute the KeyboardInterrupt signal

        Rebind the old signal handler for SIGINT, and re-raises the KeyboardInterrupt if
        it was triggered while the signal was muted.

        Args:
            exception_type (str): the type of the exception raised (None if no exceptions)
            exception_value (str): the value of the exception raised (None if no exceptions)
            traceback (str): traceback of the exception raised  (None if no exceptions)

        Returns:

        '''
        signal.signal(signal.SIGINT, self.old_handler)
        if self.received_signal:
            self.old_handler(*self.received_signal)

def assert_extended(condition, assert_message='', function=None):
    """
    Assert the given condition and run a function if it fails

    Try to assert condition.  Catch the AssertionError upon failure and run function if it
    is provided.  Raise the AssertionError afterwards.

    Args:
        condition (bool): the condition to test when asserting
        assert_message (str, optional): the message to print when the assertion fails, defaults to
            empty string
        function (func, optional): the function to run if the assertion fails (should not take
            any arguments), defaults to None

    Returns:
        bool: True if the assertion can be made

    Raises:
        AssertionError: Occurs when the condition asserted is False, should never happen
    """
    try:
        if assert_message:
            assert condition, assert_message
        else:
            assert condition
        return True
    except AssertionError:
        if function:
            function()
        raise
