# What is that?

This repository is a python module for running repetitive and independent code snippets either incrementally in a for
loop, or concurrently in dedicated processes, just by changing a boolean argument. This module is intended to increase
the performances of the whole program, while keeping the possibility to run it step by step for debugging purposes.

# Dependencies

- multiprocessing module (`pip install --user --upgrade multiprocessing`)
- python 3.3 or higher (because it uses the [starmap function](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.starmap))

# How to use

Let's suppose 4 functions are defined:
- nice_function(a, b)
- super_function(c, d, e)
- raise_zero_division_error()
- i_am_sorry(f)
```
>>> def nice_function(a, b) -> None:
...     print(f"running nice_function with args {a} and {b}")
...     return
...
>>> def super_function(c, d, e) -> None:
...     print(f"running super_function with args {c}, {d} and {e}")
...     return
...
>>> def raise_zero_division_error() -> None:
...     _ = 1/0
...     return
...
>>> def i_am_sorry(f) -> None:
...     print(f"I am sorry, with arg {f}")
...     return
...
```
Now, let's schedule jobs by appending callables with their arguments:
```
>>> from multiprocessor import Job, Multiprocessor
>>>
>>> j1, j2, j3 = Job(), Job(), Job()
>>>
>>> j1.append_normal_task(nice_function, ("foo", "bar"))
>>>
>>> j2.append_normal_task(nice_function, ("bloob", "kamoulox"))
>>> j2.append_normal_task(super_function, ("charmander", "bulbasaur", "pikachu"))
>>>
>>> j3.append_normal_task(raise_zero_division_error)
>>> j3.append_exception_to_catch(ZeroDivisionError)
>>> j3.append_forgiveness_task(i_am_sorry, ("Running out of ideas",))
>>>
>>> jobs = (j1, j2, j3)
```
Now, all the jobs can be run either concurrently in dedicated processes:
```
>>> finished_jobs = Multiprocessor.run(jobs, parallelize=True, number_of_processes=3)
running nice_function with args foo and bar
running nice_function with args bloob and kamoulox
running super_function with args charmander, bulbasaur and pikachu
I am sorry, with arg Running out of ideas
```
Or one by one through a for loop:
```
finished_jobs = Multiprocessor.run(jobs, parallelize=False)
running nice_function with args foo and bar
running nice_function with args bloob and kamoulox
running super_function with args charmander, bulbasaur and pikachu
I am sorry, with arg Running out of ideas
```

# How to use (Details)

Here is the definition of the `Multiprocessor.run` method:
```
@classmethod
def run(cls, jobs: (list, tuple), parallelize: bool = True, number_of_processes: int = 0) -> list:
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
```

# Limitations

It is currently not possible to redirect the return result of a job function to another function inside this job.
Each function in a job must be independent.