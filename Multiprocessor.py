from Job import Job



class Multiprocessor(object):
    """
    This class handles the parallelization (or not) of independent pieces of code.

    The problem to solve is the following. The multiprocessing library used by this class is
    a very powerful library for distributing procedures into concurrent sub-processes. But the
    counterpart is it may have unexpected side effects, and it may be difficult to debug: when
    the code of a child process crashes, it yields a huge stack trace.

    For that reason, we may want to run our sub-routines either in parallel, or incrementally
    inside the main process, but just by changing one boolean parameter. The treatment is different
    because if we want parallelization, we need to map a function in a Pool of the multiprocessing
    library, but if we want an incremental processing, a simple for loop is enough.

    As all this stuff is quite complicated, this dedicated module has been created. The main idea is
    to define a series of jobs (see Job class of this module), and pass it to the Multiprocessor run method.
    The parameters of the run method allow to either distribute the jobs into concurrent processes, or
    run them incrementally in a for loop.

    If run incrementally, the multiprocessing ligrary is not imported, which saves memory.

    IMPORTANT NOTE: This class is intended to work with instances of the class Job

    Example of use:

    >>> from NasaFramework.utils.multiprocessor.Job import Job
    >>>
    >>> class Car(object):
    ...
    ...     def __init__(self, brand: str, color: str) -> None:
    ...         self.__brand, self.__color = brand, color
    ...         return
    ...
    ...     def drive(self, distance: float, speed: float) -> None:
    ...         print('VROOOOOOOOOM')
    ...         return
    ...
    ...     def show_off(self) -> None:
    ...         print('Yeaaah !')
    ...         return
    ...
    ...     def honk_the_horn(self) -> None:
    ...         print('BEEEP')
    ...         return
    >>>
    >>> job_1 = Job\
    ...     (
    ...         class_ = Car,
    ...         init_arguments = ('red', 'Volkswagen'),
    ...         methods_and_arguments = {Car.drive: (5.5, 10.4), Car.show_off: tuple()}
    ...         exceptions_to_catch = (RuntimeError, OSError),
    ...         methods_arguments_to_run_if_shit_happens = {Car.honk_the_horn: tuple()}
    ...     )
    >>>
    >>> job_2 = Job\
    ...     (
    ...         class_ = Car,
    ...         init_arguments = ('black', 'Mercedes'),
    ...         methods_and_arguments = {Car.drive: (3.8, 11.2), Car.honk_the_horn: tuple()}
    ...     )
    >>>
    >>> jobs = [job_1, job_2]

    The following line runs both the jobs in parallel by spawning up to 2 processes:
    >>> job_results_1 = Multiprocessor.run(jobs, parallelize=True, number_of_processes=2)

    The following line runs both the jobs one by one in a for loop:
    >>> job_results_2 = Multiprocessor.run(jobs, parallelize=False)

    At the end, you get the same results:
    >>> job_results_1 == job_results_2
    True
    """


    def __new__(cls) -> type:
        """
        @param cls:         type        Address of the Multiprocessor class (implicit parameter)

        @return:            type        The Multiprocessor class (not an object derived from it, but the class itself!)

        This class is not meant to instantiate objects. returning the class itself if someone tries to
        create a new instance.
        """
        return cls




#   ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗     ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
#   ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝     ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
#   ██████╔╝██║   ██║██████╔╝██║     ██║██║          ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
#   ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║          ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
#   ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
#   ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝


    @classmethod
    def run(cls, jobs: (list, tuple), parallelize: bool = True, number_of_processes: int = 0) -> list:
        """
        @param cls:                     type            Address of the Multiprocessor class (implicit parameter)
        @param jobs:                    list            A list of instances of the Job class
        @param parallelize:             bool = True     Should the jobs be distributed into sub-processes?
        @param number_of_processes:     int = 0         Max number of processes to spawn.
                                                        Ignored if @parallelize = False
                                                        If 0 or negative, then = number of cpu cores.

        @return:                        list            A list on the results of self.__jobs, on the form:
                                                        [(job.results, job.results_if_shit_happened)]

        This method triggers the execution of the jobs. Either they are distributed in subprocesses and
        run concurrently if @parallelize is set to True, or they are run one by one in the main procedure
        process through a for loop.

        note: If there is only 1 job to do in the @jobs list parameter, this job is done in the main procedure
        without spawning a dedicated process, even if @parallelize is set to True
        """
        if parallelize and len(jobs) > 1:
            from multiprocessing import Pool, cpu_count
            if number_of_processes <= 0:
                number_of_processes = cpu_count()
            mapped_arguments = [(job,) for job in jobs]
            with Pool(number_of_processes) as swimming:  # Because it is the swimming Pool... hahaha !
                jobs_done = swimming.starmap(cls._wrapper, mapped_arguments)
            jobs = jobs_done  # Need to update, because jobs were updated into child processes. Not in the parent
        else:
            for job in jobs:
                cls._wrapper(job)
        return jobs  # cls.__set_up_results(jobs)




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

        @return:            list            A list on the results of self.__jobs, on the form:
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
    def _wrapper(job: Job) -> Job:
        """
        @param job:         Job         An instance of the class Job

        @return:            Job         The same instance as the one passed in parameter.

        This method executes in practice the procedure described in a Job instance.
        Normally, instances of Job contains a result section so in theory, we don't need
        to return anything. But in the case that jobs are run into subprocesses, the Job
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
            job.ask_forgiveness(error)
        return job


        # # Instantiation
        # try:
        #     instance = job.class_(*job.init_arguments)
        # except job.exceptions_to_catch as error:
        #     job.log_error(job.class_.__init__, error)
        #     return job
        #
        # # Run all the methods one by one
        # try:
        #     for method, arguments in job.methods_and_arguments.items():
        #         result = getattr(instance, method.__name__)(*arguments)  # Method is called by introspection
        #         job.add_result(method, result)
        # except job.exceptions_to_catch as error:
        #     job.log_error(method, error)
        #     for exception_method, exception_arguments in job.methods_arguments_to_run_if_shit_happens.items():
        #         result = getattr(instance, exception_method.__name__)(*exception_arguments)
        #         job.ask_forgiveness(exception_method, result)
        #
        # return job
