# Multiprocessor Module Documentation

## Overview


The `multiprocessor` module provides utilities to easily manage and execute tasks in parallel or incrementally without
hassle. It offers three primary classes: `Task`, `Job` and `Multiprocessor`.

The `Task` class is mainly used internally and is used to describe a python callable, store its arguments and its
return value, if any.

The `Job` class lets users define a series of tasks with optional exception handling and fallback tasks objects.

The `Multiprocessor` class allows these jobs to be executed either concurrently across multiple cores or incrementally
within the main process.

## Installation

```bash
git clone https://github.com/Che5hireC4t/multiprocessor.git
```

## Key Features

1. **Flexible Parallelization**: With a single parameter switch, you can choose between parallel and incremental execution.
2. **Exception Handling**: The `Job` class has built-in exception handling, allowing you to define fallback tasks for specific exceptions.
3. **Memory Efficiency**: When running tasks incrementally, the multiprocessing library isn't imported, saving memory.
4. **User-friendly Results Presentation**: Results are returned in a consistent format regardless of execution mode.

## Basic Usage

### Setup

Let's assume you have the following class:

```python
class Car(object):

    def __init__(self, brand: str, color: str) -> None:
        self.__brand, self.__color = brand, color
        return

    def drive(self, distance: float, speed: float) -> None:
        print('VROOOOOOOOOM')
        return

    def being_stuck_in_traffic_jams(self) -> None:
        raise OverflowError('Fucking jams')

    def show_off(self) -> None:
        print('Yeaaah !')
        return

    def honk_and_curse(self) -> None:
        print('BEEEP!!!!!')
        return
```

### Defining Jobs

To use this module, start by defining a series of tasks using the `Job` class:

```python
from multiprocessor import Job

j1, j2, j3 = Job(), Job(), Job()
c1, c2, c3 = Car('Volkswagen', 'grey'), Car('Mercedes', 'black'), Car('Audi', 'white')

for job, car in {j1: c1, j2: c2, j3: c3}.items():
    job.append_normal_task(car.drive, (10, 20))  # You don't have to put same values for each job.
    job.append_normal_task(car.show_off, tuple())
    job.append_normal_task(car.being_stuck_in_traffic_jams, tuple())
    job.append_exception_to_catch(OverflowError)
    job.append_forgiveness_task(car.honk_and_curse, tuple())

jobs = (j1, j2, j3)
```

### Running Jobs

You can run these jobs either in parallel or incrementally using the `Multiprocessor` class:

```python
from multiprocessor import Multiprocessor

# The following line runs all the job_generator in parallel by spawning up to 3 processes:
job_results_1 = Multiprocessor.run(jobs, parallelize=True, number_of_processes=3)

# The following line runs both the job_generator one by one in a for loop without spawning any new process:
job_results_2 = Multiprocessor.run(jobs, parallelize=False)

# At the end, you get the same results:
job_results_1 == job_results_2  # True
```

## Examples

Detailed examples can be found within the module docstrings. Here's a brief example:

```python
from multiprocessor import Job, Multiprocessor

def task_function(a, b):
    return a + b

job = Job()
job.append_normal_task(task_function, (1, 2))
results = Multiprocessor.run([job], parallelize=True)
```

## Important Notes

1. The `Multiprocessor` class is designed not to be instantiated. Instead, it offers class and static methods for direct usage.
2. Always ensure the callable functions provided to the `Job` class do not have any side effects or shared states to ensure thread-safety.
3. When using the multiprocessing library, make sure to guard your main execution using `if __name__ == '__main__':`.
4. It is currently not possible to redirect the return result of a job function to another function inside this job.
Each function in a job must be independent.

## License

This module is licensed under the GPL-3.0 License. Please see the `LICENSE` file for more information.
