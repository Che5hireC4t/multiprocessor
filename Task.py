class Task(object):
    """
    A class that represents a task containing a callable and its arguments.

    :ivar __callable: The function or method to be executed.
    :ivar __arguments: Arguments for the callable.
    :ivar __return_value: The value returned after executing the callable, if any.
    :ivar __exception_raised: Any exception that was raised while executing the callable.

    Example of use:
    >>> t = Task(print, ("test",))
    """

    __slots__ = ('__callable', '__arguments', '__return_value', '__exception_raised')



    def __init__(self, callable_: callable, arguments: tuple = tuple()) -> None:
        """
        Initialize a new Task instance.

        :param callable_: The function or method to be executed.
        :type callable_: callable

        :param arguments: The arguments for the callable. Defaults to an empty tuple.
        :type arguments: tuple
        """
        assert callable(callable_), f"'callable_' argument must be callable. However, is of type {type(callable_)}."
        self.__callable = callable_
        self.__arguments = tuple(arguments)
        self.__return_value = None
        self.__exception_raised = None
        return



    if __debug__:
        def __repr__(self) -> str:
            """
            Representation of the Task instance, for debugging.
            """
            return f"{self.__class__.__name__}({self.__callable.__name__}, {self.__arguments})"




#   ██████╗  ██████╗   ██████╗  ██████╗  ███████╗ ██████╗ ████████╗ ██╗ ███████╗ ███████╗
#   ██╔══██╗ ██╔══██╗ ██╔═══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗╚══██╔══╝ ██║ ██╔════╝ ██╔════╝
#   ██████╔╝ ██████╔╝ ██║   ██║ ██████╔╝ █████╗   ██████╔╝   ██║    ██║ █████╗   ███████╗
#   ██╔═══╝  ██╔══██╗ ██║   ██║ ██╔═══╝  ██╔══╝   ██╔══██╗   ██║    ██║ ██╔══╝   ╚════██║
#   ██║      ██║  ██║ ╚██████╔╝ ██║      ███████╗ ██║  ██║   ██║    ██║ ███████╗ ███████║
#   ╚═╝      ╚═╝  ╚═╝  ╚═════╝  ╚═╝      ╚══════╝ ╚═╝  ╚═╝   ╚═╝    ╚═╝ ╚══════╝ ╚══════╝


    def __get_callable(self) -> callable:
        """
        Get the task callable. This property is read-only.
        """
        return self.__callable

    callable_ = property(fget=__get_callable, doc=f"{__get_callable.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_arguments(self) -> tuple:
        """
        Get the arguments used with the callable. This property is read-only.
        """
        return self.__arguments

    arguments = property(fget=__get_arguments, doc=f"{__get_arguments.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_return_value(self):
        """
        Get the return value after executing the callable.
        """
        return self.__return_value

    def __set_return_value(self, value) -> None:
        """
        Set the return value for the callable.
        """
        self.__return_value = value
        return

    return_value = property \
        (
            fget=__get_return_value,
            fset=__set_return_value,
            doc=f"{__get_return_value.__doc__}\n\n{__set_return_value.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    def __get_exception_raised(self) -> BaseException:
        """
        Get the exception raised during callable execution, if any.
        """
        return self.__exception_raised

    def __set_exception_raised(self, value: BaseException) -> None:
        """
        Set the exception raised during callable execution.

        :param value: The exception raised.
        :type value: BaseException
        """
        # Ensure value is well an exception without using an if else block.
        try:
            raise value
        except value.__class__ as error:
            self.__exception_raised = error
        return

    exception_raised = property \
        (
            fget=__get_exception_raised,
            fset=__set_exception_raised,
            doc=f"{__get_exception_raised.__doc__}\n\n{__set_exception_raised.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    if __debug__:
        def __get_callable_name(self) -> str:
            """
            Get the name of the callable. For debugging. This property is read-only.
            """
            return self.__callable.__name__

        callable_name = property(fget=__get_callable_name, doc=f"{__get_callable_name.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------
