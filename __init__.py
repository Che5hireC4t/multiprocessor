"""
`multiprocessor` Module
=======================

This module provides tools to manage and execute tasks, both in parallel and incrementally.
The primary components of the module are the `Job` and `Multiprocessor` classes.

The `Job` class allows you to define, schedule, and manage lists of tasks. It provides
exception handling and fallback task mechanisms to ensure that tasks can be recovered or
alternative actions can be taken when something unexpected occurs. Each job maintains
a list of tasks to be executed, a list of exceptions to handle, and a list of fallback tasks
to run if any exceptions are encountered.

The `Multiprocessor` class handles the parallelization (or not) of independent pieces of code.
It leverages the `multiprocessing` library to distribute tasks into concurrent subprocesses.
However, it provides a flexible mechanism to choose between parallel execution and incremental
execution in a single process. By switching a boolean parameter, users can decide how tasks
should be executed, offering flexibility in terms of resources and debugging.

Additionally, the `Multiprocessor` class is designed to work seamlessly with the `Job` class.
Users can define a series of job_generator and then pass them to the `Multiprocessor` for execution.

Main Components
---------------
1. `Task`: A class that represents a task containing a callable and its arguments.
2. `Job`: A class that encapsulates a list of tasks to be executed. Offers exception handling and fallback mechanisms.
3. `Multiprocessor`: A class that provides mechanisms for executing tasks,
                     either in parallel using subprocesses or incrementally.

Usage Examples:
---------------
1. Define tasks using the `Job` class.
2. Define whether tasks should be run in parallel or incrementally using the `Multiprocessor` class.
3. Execute the job_generator and retrieve the results.

You can view a fully functional example in the docstring of `Multiprocessor` class

Note: The `Multiprocessor` class is designed to work seamlessly with instances of the `Job` class.
This module provides both parallel and incremental execution capabilities, making it versatile for various scenarios.

For detailed examples and further documentation, please refer to the docstrings of the respective classes and methods.
"""

# This is just a memo for myself in order to handle versioning properly:
# https://betterprogramming.pub/why-versioning-is-important-and-how-to-do-it-686ce13b854f?gi=81d210140bbf
__version__ = '1.0.0'

from .Results import Results
from .Task import Task
from .Job import Job
from .Multiprocessor import Multiprocessor
