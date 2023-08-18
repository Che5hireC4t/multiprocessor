from . import Task



class Job(object):
    """
    A class that represents a job consisting of a list of tasks to execute.
    This Job class provides a mechanism to schedule and manage a list of tasks to be run.
    Additionally, it offers functionality to define exception handling and fallback tasks
    should any of the primary tasks fail.

    :ivar __tasks_to_do: The list of tasks to be executed.
    :ivar __exceptions_to_catch: The exceptions that this job intends to handle.
    :ivar __tasks_to_do_if_shit_happens: List of tasks to be executed if exceptions occur.
    :ivar __ongoing_task: The task that is currently being executed.


    Example 1:

    >>> def add(a, b) -> int:
    ...     return a + b

    >>> def mul(a, b) -> int:
    ...     return a * b

    >>> job = Job()
    >>> job.append_normal_task(add, (1, 1))
    >>> job.append_normal_task(mul, (2, 3))
    >>> job.run()
    >>> completed_tasks = job.tasks_to_do
    >>> [print(t.return_value) for t in completed_tasks]
    2
    6


    Example 2:

    >>> def divide_by_zero():
    ...     return 1/0

    >>> def ask_forgiveness() -> str:
    ...     return 'Oops, sorry!'

    >>> job = Job()
    >>> job.append_normal_task(add, (1, 1))
    >>> job.append_normal_task(divide_by_zero, tuple())
    >>> job.append_normal_task(mul, (2, 3))
    >>> job.append_exception_to_catch(ZeroDivisionError)
    >>> job.append_forgiveness_task(ask_forgiveness, tuple())
    >>> job.run()
    >>> completed_tasks = job.tasks_to_do
    >>> completed_error_tasks = job.tasks_to_do_if_shit_happens
    >>> [print(t.return_value) for t in completed_tasks]
    2
    None
    None
    >>> [print(t.return_value) for t in completed_error_tasks]
    'Oops, sorry!'
    """

    __slots__ = ('__tasks_to_do', '__exceptions_to_catch', '__tasks_to_do_if_shit_happens', '__ongoing_task')



    def __init__(self) -> None:
        """
        Initialize a new Job instance.

        This method sets up the initial state of the Job object by
        preparing empty lists for tasks, exception handling, and fallback tasks.
        It also initializes an attribute to keep track of the task currently being executed.
        """
        self.__tasks_to_do = list()
        self.__exceptions_to_catch = list()
        self.__tasks_to_do_if_shit_happens = list()
        self.__ongoing_task = None
        return




#   ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗     ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
#   ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝     ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
#   ██████╔╝██║   ██║██████╔╝██║     ██║██║          ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
#   ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║          ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
#   ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
#   ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝


    def append_normal_task(self, callable_: callable, arguments: tuple = tuple()) -> None:
        """
        Add a standard task to the job's execution list.

        :param callable_: The function or method to be executed.
        :param arguments: Optional arguments for the callable.
        """
        self.__tasks_to_do.append(Task(callable_, arguments))
        return



    def clear_normal_tasks(self) -> None:
        """Purge all standard tasks from the job's execution list."""
        self.__tasks_to_do = list()
        return



    def append_forgiveness_task(self, callable_: callable, arguments: tuple = tuple()) -> None:
        """
        Add a fallback task to execute if any standard tasks raise exceptions.

        These tasks serve as a 'Plan B', providing a means to attempt recovery or alternative actions
        when things don't go as planned.

        :param callable_: The function or method to be executed in case of an exception.
        :param arguments: Optional arguments for the callable.
        """
        self.__tasks_to_do_if_shit_happens.append(Task(callable_, arguments))
        return



    def clear_forgiveness_tasks(self) -> None:
        """Purge all fallback tasks from the job's list."""
        self.__tasks_to_do_if_shit_happens = list()
        return



    def append_exception_to_catch(self, exception) -> None:
        """
        Designate exceptions that the job will handle.

        This method defines which exceptions, when raised during the execution of tasks,
        should trigger the fallback tasks.

        :param exception: The exception type or a collection of exception types.
        """
        if type(exception) in (list, tuple, set, frozenset):
            if not all(issubclass(e, BaseException) for e in exception):
                raise TypeError('All the objects passed as argument must be subclasses of BaseException.')
            self.__exceptions_to_catch.extend(exception)
            return
        if issubclass(exception, BaseException):
            self.__exceptions_to_catch.append(exception)
            return
        return



    def clear_exceptions(self) -> None:
        """Purge all designated exceptions from the job's list."""
        self.__exceptions_to_catch = list()



    def run(self) -> None:
        """
        Execute all the standard tasks in sequence.

        This method runs each task in the order they were added. If a task raises an exception
        that the Job is set to handle, the fallback tasks will be triggered.
        """
        for task in self.__tasks_to_do:
            self.__ongoing_task = task
            return_value = task.callable_(*task.arguments)
            task.return_value = return_value
        return



    def ask_forgiveness(self, exception_raised: BaseException) -> None:
        """
        Handle an exception by executing all the fallback tasks.

        When an exception is raised, this method can be called to run the fallback tasks
        and attempt recovery or alternative actions.

        The name of that method comes from the python "EAFP" principle
        (Easier to Ask for Forgiveness than Permission).

        :param exception_raised: The exception that was triggered.
        """
        self.__ongoing_task.exception_raised = exception_raised
        for task in self.__tasks_to_do_if_shit_happens:
            return_value = task.callable_(*task.arguments)
            task.return_value = return_value
        return




#   ██████╗  ██████╗   ██████╗  ██████╗  ███████╗ ██████╗ ████████╗ ██╗ ███████╗ ███████╗
#   ██╔══██╗ ██╔══██╗ ██╔═══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗╚══██╔══╝ ██║ ██╔════╝ ██╔════╝
#   ██████╔╝ ██████╔╝ ██║   ██║ ██████╔╝ █████╗   ██████╔╝   ██║    ██║ █████╗   ███████╗
#   ██╔═══╝  ██╔══██╗ ██║   ██║ ██╔═══╝  ██╔══╝   ██╔══██╗   ██║    ██║ ██╔══╝   ╚════██║
#   ██║      ██║  ██║ ╚██████╔╝ ██║      ███████╗ ██║  ██║   ██║    ██║ ███████╗ ███████║
#   ╚═╝      ╚═╝  ╚═╝  ╚═════╝  ╚═╝      ╚══════╝ ╚═╝  ╚═╝   ╚═╝    ╚═╝ ╚══════╝ ╚══════╝


    def __get_normal_tasks(self) -> tuple[Task, ...]:
        """
        Retrieve all standard tasks currently in the job's execution list.
        This property is read-only.
        """
        return tuple(self.__tasks_to_do)

    tasks_to_do = property(fget=__get_normal_tasks, doc=f"{__get_normal_tasks.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_tasks_if_shit_happens(self) -> tuple[Task, ...]:
        """
        Retrieve all fallback tasks currently in the job's list.
        This property is read-only.
        """
        return tuple(self.__tasks_to_do_if_shit_happens)

    tasks_to_do_if_shit_happens = property \
        (
            fget=__get_tasks_if_shit_happens,
            doc=f"{__get_tasks_if_shit_happens.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    def __get_exceptions(self) -> tuple:
        """
        Retrieve all exceptions that the job is set to handle.
        This property is read-only.
        """
        if len(self.__exceptions_to_catch) == 0:
            return BaseException,
        return tuple(self.__exceptions_to_catch)

    exceptions_to_catch = property(fget=__get_exceptions, doc=f"{__get_exceptions.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------
