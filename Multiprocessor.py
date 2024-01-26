from . import Job
from . import Results


class Multiprocessor(object):
    """
    This class handles the parallelization (or not) of independent pieces of code.

    The problem to solve is the following. The multiprocessing library used by this class is
    a very powerful library for distributing procedures into concurrent sub-processes. But the
    counterpart is it may have unexpected side effects, and it may be difficult to debug: when
    the code of a child process crashes, it yields a huge stack trace.

    Another problem is we may want to run pieces of code either in parallel or not, at will,
    depending on if we have the ressources to do it or not.

    For that reason, we may want to run our sub-routines either in parallel, or incrementally
    inside the main process, but just by changing one boolean parameter. The treatment is different
    because if we want parallelization, we need to map a function in a Pool of the multiprocessing
    library, but if we want an incremental processing, a simple for loop is enough.

    As all this stuff is quite complicated, this dedicated module has been created. The main idea is
    to define a series of job_generator (see Job class of this module), and pass it to the Multiprocessor run method.
    The parameters of the run method allow to either distribute the job_generator into concurrent processes, or
    run them incrementally in a for loop.

    If run incrementally, the multiprocessing ligrary is not imported, which saves memory.

    IMPORTANT NOTE: This class is intended to work with instances of the class Job

    Example of use (This example has been tested and works):

    >>> import Job
    >>>
    >>> class Car(object):
    ...
    ...     def __init__(cls, brand: str, color: str) -> None:
    ...         cls.__brand, cls.__color = brand, color
    ...         return
    ...
    ...     def drive(cls, distance: float, speed: float) -> None:
    ...         print('VROOOOOOOOOM')
    ...         return
    ...
    ...     def being_stuck_in_traffic_jams(cls) -> None:
    ...         raise OverflowError('Fucking jams')
    ...
    ...     def show_off(cls) -> None:
    ...         print('Yeaaah !')
    ...         return
    ...
    ...     def honk_and_curse(cls) -> None:
    ...         print('BEEEP!!!!!')
    ...         return

    >>> j1, j2, j3 = Job(), Job(), Job()
    >>> c1, c2, c3 = Car('Volkswagen', 'grey'), Car('Mercedes', 'black'), Car('Audi', 'white')
    >>> for job, car in {j1: c1, j2: c2, j3: c3}.items():
    ...     job.append_normal_task(car.drive, (10, 20))  # You don't have to put same values for each job.
    ...     job.append_normal_task(car.show_off, tuple())
    ...     job.append_normal_task(car.being_stuck_in_traffic_jams, tuple())
    ...     job.append_exception_to_catch(OverflowError)
    ...     job.append_forgiveness_task(car.honk_and_curse, tuple())

    >>> job_generator = (j1, j2, j3)

    The following line runs all the job_generator in parallel by spawning up to 3 processes:
    >>> job_results_1 = Multiprocessor.run(job_generator, parallelize=True, number_of_processes=3)

    The following line runs both the job_generator one by one in a for loop without spawning any new process:
    >>> job_results_2 = Multiprocessor.run(job_generator, parallelize=False)

    At the end, you get the same results:
    >>> job_results_1 == job_results_2
    True
    """

    __slots__ = ('__job_generator', '__parallelize', '__number_of_processes', '__result_extractor_function')

    __GENERATOR = type((_ for _ in range(0)))




#   ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗     ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
#   ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝     ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
#   ██████╔╝██║   ██║██████╔╝██║     ██║██║          ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
#   ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║          ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
#   ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
#   ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝


    def __init__ \
            (
                self,
                job_generator: __GENERATOR[Job],
                extractor_function: callable,
                parallelize: bool = True,
                number_of_processes: int = 0
            ) -> None:
        """
        Initialize the Multiprocessor object.

        This method sets up the Multiprocessor with the necessary parameters
        to handle job execution either in parallel or sequentially.

        This constructor performs validation on the input arguments to ensure they meet the requirements for processing.
        If the validation fails, it raises a TypeError with a detailed error message.

        The `job_generator` must be an iterable of Job objects, `extractor_function` must be callable,
        `parallelize` must be a boolean, and `number_of_processes` must be an integer.

        :param job_generator: An iterable of Job objects, preferably a generator,
                              that produces the jobs to be processed.
        :type job_generator:  __GENERATOR[Job]


        :param extractor_function: A callable that extracts results from the processed jobs.
                                   This function should return a Result object.
        :type extractor_function:  callable


        :param parallelize: A boolean flag indicating whether to run the jobs in parallel (True) or sequentially (False)
                            Defaults to True.
        :type parallelize:  bool, optional


        :param number_of_processes: The number of processes to use for parallel execution.
                                    If set to 0, the number of processes is automatically determined. Default to 0.
        :type number_of_processes:  int, optional


        :raises TypeError: If the input arguments do not meet the expected types or requirements.



        Example:
            >>> job_generator = (job1, job2, job3)  # Where job1, job2, job3 are Job instances.
            >>> extractor = lambda job: job.result  # An example extractor function.
            >>> processor = Multiprocessor(job_generator, extractor, True, 4)
        """
        if hasattr(job_generator, '__iter__') \
                and isinstance(parallelize, bool) \
                and isinstance(number_of_processes, int) \
                and callable(extractor_function):
            self.__job_generator = job_generator
            self.__parallelize = parallelize
            self.__number_of_processes = number_of_processes
            self.__result_extractor_function = extractor_function
            return
        problems = set()
        if not hasattr(job_generator, '__iter__'):
            problems.add('- job_generator must be an iterable of Jobs and preferably a generator.')
        if not isinstance(parallelize, bool):
            problems.add(f"- parallelize must be a boolean value. Got {type(parallelize).__name__} instead.")
        if not isinstance(number_of_processes, int):
            msg = f"- number_of_processes must be an integer value. Got {type(number_of_processes).__name__} instead."
            problems.add(msg)
        if not callable(extractor_function):
            problems.add('- extractor_function must be a callable returning a Result object.')
        n = "\n"
        error_message = f"Error with input arguments. The following problems were raised:\n\n{n.join(problems)}"
        raise TypeError(error_message)



    def run(self) -> tuple[Results | None]:
        """
        @return:                        list            A list on the results of cls.__jobs, on the form:
                                                        [(job.results, job.results_if_shit_happened)]

        This method triggers the execution of the jobs. Either they are distributed in subprocesses and
        run concurrently if @parallelize is set to True, or they are run one by one in the main procedure
        process through a for loop.

        note: If there is only 1 job to do in the @jobs list parameter, this job is done in the main procedure
        without spawning a dedicated process, even if self.__parallelize is set to True
        """
        if self.__parallelize:
            from multiprocessing import Pool, cpu_count
            if self.__number_of_processes <= 0:
                number_of_processes = cpu_count()
            mapped_arguments = [(job,) for job in self.__job_generator]
            with Pool(number_of_processes) as swimming:  # Because it is the swimming Pool... hahaha !
                results = swimming.starmap(self._wrapper, mapped_arguments)
            return tuple(results)
        else:
            results = list()
            for job in self.__job_generator:
                result = self._wrapper(job)
                results.append(result)
        return tuple(results)




#   ██████╗ ██████╗ ██╗██╗   ██╗        ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
#   ██╔══██╗██╔══██╗██║██║   ██║        ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
#   ██████╔╝██████╔╝██║██║   ██║        ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
#   ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝        ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
#   ██║     ██║  ██║██║ ╚████╔╝ ██╗     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
#   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝


    @staticmethod
    def __set_up_results(jobs: list) -> list:
        """
        @param jobs:        list            A list of instances of the Job class

        @return:            list            A list on the results of cls.__jobs, on the form:
                                            [(job.results, job.results_if_shit_happened)]

        Take the job results, and present them in a user-readable list.
        """
        results = \
            [
                (job.results, job.results_if_shit_happened)
                if any([isinstance(item, BaseException) for item in job.results.values()])
                else (job.results, None)
                for job in jobs
            ]
        results = \
            [
                next(reversed(good_result_dict.values()))
                if bad_result_dict is None
                else next(reversed(bad_result_dict.values()))
                for good_result_dict, bad_result_dict in results
            ]
        return results



    @staticmethod
    def _wrapper(job: Job) -> Results | None:
        """
        @param job:         Job         An instance of the class Job

        @return:            Job         The same instance as the one passed in parameter.

        This method executes in practice the procedure described in a Job instance.
        Normally, instances of Job contains a result section so in theory, we don't need
        to return anything. But in the case that job_generator are run into subprocesses, the Job
        instances are updated into child processes, not in the parent one. If we don't
        return the updated instance (to the parent process), their results will be lost.

        This method must be static, in order to run it with the multiprocessing library.

        Note for devs: however this method is strictly internal and should be private,
        it must be only protected for the purposes of Multiprocessing. Indeed, if the function
        were private (and thus starts with double underscore __), the python interpreter
        internally rename it by prepending the name of the class it belongs to (in that
        case, it will be renamed _Multiprocessor__wrapper). This causes a problem for pickling/
        unpickling the method for its transfer from the parent process to the child process
        because the multiprocessing library does not take into account this renaming process.
        Thus, the library will seek for Multiprocessor.__wrapper while the method is called
        _Multiprocessor__wrapper. The solution is to pass the method to protected, because it
        won't be renamed by the interpreter.
        """
        try:
            job.run()
        except job.exceptions_to_catch as error:
            print(error)
            job.ask_forgiveness(error)
        for task in job.tasks_to_do:
            return_value = task.return_value
            if isinstance(return_value, Results):
                return return_value
        for task in job.tasks_to_do_if_shit_happens:
            return_value = task.return_value
            if isinstance(return_value, Results):
                return return_value
        return None
