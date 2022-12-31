class Task(object):

    __slots__ = ('__callable', '__arguments', '__return_value', '__exception_raised')

    def __init__(self, callable_: callable, arguments: tuple = tuple()) -> None:
        assert callable(callable_), f"'callable_' argument must be callable. However, is of type {type(callable_)}."
        self.__callable = callable_
        self.__arguments = tuple(arguments)
        self.__return_value = None
        self.__exception_raised = None
        return

    if __debug__:
        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.__callable.__name__}, {self.__arguments})"




#   ██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗ ███████╗███████╗
#   ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║ ██╔════╝██╔════╝
#   ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║ █████╗  ███████╗
#   ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║ ██╔══╝  ╚════██║
#   ██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║   ██║ ███████╗███████║
#   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══════╝╚══════╝

    def __get_callable(self) -> callable:
        return self.__callable

    callable_ = property(fget=__get_callable, doc=f"{__get_callable.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    if __debug__:
        def __get_callable_name(self) -> str:
            return self.__callable.__name__

        callable_name = property(fget=__get_callable_name, doc=f"{__get_callable_name.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_arguments(self) -> tuple:
        return self.__arguments

    arguments = property(fget=__get_arguments, doc=f"{__get_arguments.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_return_value(self):
        return self.__return_value

    def __set_return_value(self, value) -> None:
        self.__return_value = value
        return

    return_value = property\
        (
            fget=__get_return_value,
            fset=__set_return_value,
            doc=f"{__get_return_value.__doc__}\n\n{__set_return_value.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    def __get_exception_raised(self) -> BaseException:
        return self.__exception_raised

    def __set_exception_raised(self, value: BaseException) -> None:
        try:  # Ensure value is well an exception without using an if else block.
            raise value
        except value.__class__ as error:
            self.__exception_raised = error
        return

    exception_raised = property\
        (
            fget=__get_exception_raised,
            fset=__set_exception_raised,
            doc=f"{__get_exception_raised.__doc__}\n\n{__set_exception_raised.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------



class Job(object):
    """
    This class represents task to do. It is intended to schedule a sub-procedure in order
    to be executed for instance by a sub-process.



    ███████╗ ██╗      ██████╗ ████████╗ ███████╗
    ██╔════╝ ██║     ██╔═══██╗╚══██╔══╝ ██╔════╝
    ███████╗ ██║     ██║   ██║   ██║    ███████╗
    ╚════██║ ██║     ██║   ██║   ██║    ╚════██║
    ███████║ ███████╗╚██████╔╝   ██║    ███████║
    ╚══════╝ ╚══════╝ ╚═════╝    ╚═╝    ╚══════╝

    __tasks_to_do                                         type            A class to instantiate
    __exceptions_to_catch                                tuple           The arguments of @__class.__init__
    __tasks_to_do_if_shit_happens                         OrderedDict     An ordered dictionary containing a series of
    __ongoing_task




    ██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗ ███████╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║ ██╔════╝██╔════╝
    ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║ █████╗  ███████╗
    ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║ ██╔══╝  ╚════██║
    ██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║   ██║ ███████╗███████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══════╝╚══════╝

    tasks_to_do                     -->     __tasks_to_do                       Read Only
    tasks_to_do_if_shit_happens     -->     __tasks_to_do_if_shit_happens       Read Only
    exceptions_to_catch             -->     __exceptions_to_catch               Read Only
    """

    __slots__ = ('__tasks_to_do', '__exceptions_to_catch', '__tasks_to_do_if_shit_happens', '__ongoing_task')



    def __init__(self) -> None:
        self.__tasks_to_do = list()
        self.__exceptions_to_catch = list()
        self.__tasks_to_do_if_shit_happens = list()
        self.__ongoing_task = None
        return



    def append_normal_task(self, callable_: callable, arguments: tuple = tuple()) -> None:
        self.__tasks_to_do.append(Task(callable_, arguments))
        return



    def clear_normal_tasks(self) -> None:
        self.__tasks_to_do = list()
        return

    def append_forgiveness_task(self, callable_: callable, arguments: tuple = tuple()) -> None:
        self.__tasks_to_do_if_shit_happens.append(Task(callable_, arguments))
        return



    def clear_forgiveness_tasks(self) -> None:
        self.__tasks_to_do_if_shit_happens = list()
        return



    def append_exception_to_catch(self, exception) -> None:
        if type(exception) in (list, tuple, set, frozenset):
            if not all(issubclass(e, BaseException) for e in exception):
                raise TypeError('All the objects passed as argument must be subclasses of exception.')
            self.__exceptions_to_catch.extend(exception)
            return
        if issubclass(exception, BaseException):
            self.__exceptions_to_catch.append(exception)
            return
        return



    def clear_exceptions(self) -> None:
        self.__exceptions_to_catch = list()
        return



    def run(self) -> None:
        for task in self.__tasks_to_do:
            self.__ongoing_task = task
            return_value = task.callable_(*task.arguments)
            task.return_value = return_value
        return



    def ask_forgiveness(self, exception_raised: BaseException) -> None:
        self.__ongoing_task.exception_raised = exception_raised
        for task in self.__tasks_to_do_if_shit_happens:
            return_value = task.callable_(*task.arguments)
            task.return_value = return_value
        return



    @staticmethod
    def __do_nothing():
        pass



#   ██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗ ███████╗███████╗
#   ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║ ██╔════╝██╔════╝
#   ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║ █████╗  ███████╗
#   ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║ ██╔══╝  ╚════██║
#   ██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║   ██║ ███████╗███████║
#   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══════╝╚══════╝

    def __get_normal_tasks(self) -> tuple:
        return tuple(self.__tasks_to_do)

    tasks_to_do = property(fget=__get_normal_tasks, doc=f"{__get_normal_tasks.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_tasks_if_shit_happens(self) -> tuple:
        return tuple(self.__tasks_to_do_if_shit_happens)

    tasks_to_do_if_shit_happens = property\
        (
            fget=__get_tasks_if_shit_happens,
            doc=f"{__get_tasks_if_shit_happens.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    def __get_exceptions(self) -> tuple:
        if len(self.__exceptions_to_catch) == 0:
            return BaseException,
        return tuple(self.__exceptions_to_catch)

    exceptions_to_catch = property(fget=__get_exceptions, doc=f"{__get_exceptions.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------
