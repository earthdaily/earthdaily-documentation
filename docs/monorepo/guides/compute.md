---
title: Compute Guide
description: Parallelize Python computations at scale using the EarthOne Compute API and cloud infrastructure
keywords:
  - compute
  - parallel processing
  - cloud computing
  - serverless functions
  - batch jobs
  - scalable compute
---

# Compute

The Compute API provides scalable compute capabilities to parallelize
your computations. It works by packaging your Python code and executing
the code on nodes hosted by EarthOne in our cloud infrastructure. These
nodes are able to access imagery at extremely high rates of throughput
which, paired with horizontal scaling, allow you to execute computations
over nearly any spatio-temporal scale.

All features described here require a recent version of the EarthOne
Python client, version 2.1.0 or later.

See [these instructions](..//installation.md) for installing the latest
client.

You can view the current status of your Compute artifacts through the
[Compute UI](https://earthone.earthdaily.com/compute).

!!! note
    For information about API Quotas and limits see our
    [Quotas & Limits page](quota.md).

## Basic Example

This basic example shows how to create a new
`Function` and invoke it to schedule a
single Job.

!!! note
    All the following examples use Python 3.10. You may need to adapt
    these to your Python version by changing the `image` argument to match
    your Python version. See `choosing-your-environment` for the available
    images.

!!! note
    The source for the entrypoint function must be available to Compute.
    These examples must be run by placing the code in a file and executing
    that file with Python.

``` python
from earthdaily.earthone.compute import Function

def hello(i):
    import geopandas

    print(geopandas)
    return "hello {}".format(i)

print("creating function")
async_func = Function(
    hello,
    name="my-compute-hello",
    image="python3.10:latest",
    cpus=0.25,
    memory=512,
    maximum_concurrency=1,
    timeout=600,
    retry_count=0,
    requirements=[
        "geopandas",
    ],
)
async_func.save()

# invoke the function
print("submitting a job")
job = async_func(5)

# print the job result and logs
print("waiting for the job to complete")
job.wait_for_completion()
print(job.result())
print(job.log())
```

We define a python function called `hello` which prints out information
about the `geopandas` package, and returns the string
hello.

Then we generate a new `Function` instance
which specifies the entrypoint function `hello`, gives the Function a
name, and specifies a Docker image that defines the environment in which
the code will be executed.

Finally, we invoke the Function object to create a
`Job`. This submits the Job to the
Function, and the reference to the Job is stored in the `job` variable.
This also triggers an instance to spin up on the backend to execute the
Job. Instance management is handled in the background. Instances are
created or destroyed as needed to match the compute resources required
by the jobs.

A few important features of the Compute API are highlighted by this
example:

- You can pass any JSON-serializable argument to a Job, e.g. arguments
  with type `str`, `dict`, `list`, `None`, or any numeric data type.
- Your can import non-standard Python packages to be used in your
  function if the packages are specified as
  `requirements` or already
  present in the image you've selected.
- You can access any logging or debugging information, including print
  statements executed inside your function, through the logs available
  using `log`.
- This example is for illustration purposes only. If you only need to
  invoke a function once, you can do so directly and with much speedier
  results without using Compute!

Logs and details for individual jobs are also available through the
[Compute UI](https://earthone.earthdaily.com/compute).

## Compute Concepts

The two main concepts in Compute are
`Function` and
`Job`. A Function is a container for your
code and defines the environment in which your code will be executed. A
Job is a single execution of your code, using parameters defined when
the Job is created and executing using the code and environment defined
by the Function. Jobs are executed asynchronously, and the results of a
Job can be retrieved once the Job has completed.

Functions can be long-lived, and are able to execute multiple Jobs
concurrently. Jobs can be created one at a time, or many at once using
the `map` method. Job completion
can be awaited individually, or in bulk using several different Function
methods. Results can be retrieved directly from successfully completed
Jobs, or iterated over using Function methods. Results and job logs can
also be retrieved directly as
[Catalog Storage Blobs](catalog.md).

Both Functions and Jobs support search interfaces with filtering and
sorting capabilities.

### Functions

`Function` instances are created using the
Function constructor, optionally followed by setting additional
attributes directly on the instance, and then calling the
`save` method to create the
Function in the EarthOne platform.

Once the function is saved it will have a
`status` value of
`BUILDING` while the
Function image is built by the backend. This process can require several
minutes to complete, and depends upon the supplied code and
requirements.

While building, it is possible to submit jobs to the Function. These
jobs will be queued and will be executed once the building process has
completed successfully. If there are any errors these jobs will never be
run. It is possible to wait for the Function to complete building using
the `wait_for_completion` method,
but only if no jobs have been submitted (otherwise the method will wait
until the Function has completed building and all submitted jobs have
completed).

When building completes successfully, the Function status will change to
`READY`, (unless
`auto_start` was set to `False`,
in which case the Function status will change to
`STOPPED`). At this point
the Function will begin to execute any jobs which have been submitted.
If there were any errors encountered during the build (for example,
incompatible or non-existent requirements were specified), the Function
status will change to
`BUILD_FAILURE`, and will
not accept or execute any jobs. The
`build_log` method can be used to
review the build log and diagnose any problems.

Normally, Functions will accept job submissions at any time, even during
building. The `enabled` attribute
(and the `enable` and
`disable` methods) can be used to
disable the submission of new jobs to the Function. This is independent
of the status of the Function. For example, a Function can be enabled
but stopped, so that no new jobs begin executing, or it can be disabled
but ready, running any previously submitted jobs which have not yet
completed.

Normally, Functions which have completed building successfully will be
ready to run any jobs which are submitted. The
`stop` method can be used to stop
a Function, preventing any new jobs from beginning execution while
currently running jobs will continue to run to completion. The
`start` method can be used to
start a Function which has been stopped, allowing any pending jobs to
begin execution. The `auto_start`
attribute can be used to control whether a Function will automatically
start when it completes building.

There is one additional Function status value
`AWAITING_BUNDLE` which
indicates that a Function has been created but the code has not yet been
uploaded by the client. This is normally a transient state, but if the
client is unable to upload the code for some reason the Function will
remain in this state, and should be deleted and recreated.

A Function which is ready but is not being used does not incur any
charges, but does consume some resources. Thus it is a best practice to
delete Functions which are no longer needed. Indeed, Functions which
have not been used for a period of 90 days will be automatically purged
by the system. A Function cannot be deleted if there are currently
running jobs.

#### Function Base Images

When creating a Function, you must specify a base imagewhich defines the
environment in which your code will be executed. When the function is
saved, the base image is used to create a new Docker image which
includes your code and any additional requirements, modules, and data
you have specified. This new image is then used to execute your code.
Once building is complete, the base image is no longer used. This means
that any subsequent changes to the base image (e.g. reassignment of
image tags) will not affect the execution of your code.

The base image is specified using a string in the form
`<pythonX.Y>:<tag>`. The `<pythonX.Y>` should correspond to the version
of python that you are using in your client to interact with the compute
service, e.g. `python3.10`. Otherwise you may encounter compatibility
issues. The `<tag>` is a string which identifies the desired version of
the base image. The `latest` tag will always refer to the most recent
version which is compatible with the EarthOne Python client that you are
using to create the function. The specific version can change in time as
a result of bug fixes, security patches, or other necessary changes.
However, it will never change in a way which is incompatible with the
EarthOne Python client that you are using to create the function. When
there is a EarthOne Python client release with breaking changes, using
`latest` with an older client will never select an image using the newer
client, but using `latest` with the newer client will select the newer
base image version.

This approach ensures that once created, nothing will alter an existing
Function's behavior, and that should you create a new instance of a
Function from the same source code, you will get the benefit of all bug
fixes and security patches in the base image without any change in
expected behavior.

The base images are supplied by the Compute platform. Please see
`choosing-your-environment` for the available images. Arbitrary
user-supplied images are not supported.

The usual policies as to support for old client versions apply. For
example, if you are using a client version which is no longer supported
according to our support policies, or you are using a Function which was
created using such a version, you may encounter issues which will not be
addressed. In such cases, you must upgrade your client to a supported
version, and recreate your Function. You can review the client version
support policies at `install-the-python-client`.

#### Function Searches

Functions can be searched for using the
`search` method. This method
returns a `Search` instance which can be
used to specify additional filtering and sorting criteria. Ultimately,
the search can be executed using the the search in an iteratable
context, or by calling the `count`
or `collect` methods.

``` python
from earthdaily.earthone.compute import Function

search = (
    Function.search()
        .param(include=["job_statistics"])
        .filter(Function.modified_date >= "2023-10-20")
        .sort("-modified_date")
)
for func in search:
    print(f"{func.name} {func.job_statistics}")

print(search.count())
print(search.collect())
```

### Jobs

`Job` instances are created using a
Function instance. They represent a single execution of the Function for
some specific set of parameters. There are two approachs to creating a
Job. The Function object is a `Callable`, so that it can be used as if
it were a normal Python function, returning a Job instance representing
the invocation which has been submitted. Alternatively, the
`map` method can be used to submit
many executions at once, returning a list of Job instances. While
semantically equivalent to submitting the same executions sequentially,
for large numbers of invocations `map` will be more efficient.

Jobs can accept both positional and keyword arguments, according to the
signature of the entrypoint function. This works quite naturally when
using the `Callable` interface. When using the `map` method, the
arguments must be passed as a iterable of iterables (the positional
args) and an iterable of mappings (the keyword args). See
`map` for further details.

Jobs are executed asynchronously, and the results of a Job can be
retrieved once the Job has completed. This can be done one job at a
time:

``` python
job = async_func(5)
job.wait_for_completion()
print(job.result())
```

or in bulk using several approaches. For example, if you wish to wait
for all jobs to complete, and then iterate over the results:

``` python
jobs = async_func.map((i,) for i in range(20))
async_func.wait_for_completion()
for job in jobs:
    print(job.result())
```

Note that this approach assumes that there are not other jobs previously
or concurrently submitted to the Function (otherwise the
`wait_for_completion` method will
wait until all outstanding jobs are done, not just the jobs of
interest). When there may be multiple groups or batches of jobs, it is
better to use the `as_completed`
method:

``` python
jobs = async_func.map((i,) for i in range(20))
for job in async_func.as_completed(jobs):
    print(job.result())
```

It is important to note that, as the name implies, the
`as_completed` will yield jobs as
they are completed, which may not be the same as the original ordering
of `jobs`. However, this approach is more efficient, as it does not
require waiting for all jobs to complete before beginning to iterate
over the results.

#### Job Lifecycle

Jobs progress through a series of states as they are created and
executed. The initial status when a job is created is
`PENDING`. This indicates that
the job is awaiting execution. The Compute service has an internal
scheduler which will assign jobs to available execution resources while
respecting concurrency constraints. Scheduling is randomized to prevent
any one user from monopolizing the resources. Once a job has been
assigned to an execution resource, its status will will change to
`RUNNING`. This indicates that
the job is currently being executed. Once the job has completed, its
status will change to either
`SUCCESS` or
`FAILURE` depending on whether it
ran to completion and returned a result, or encountered an error.
Additionally, if a running job exceeds its specified time limit (see
`timeout`), the job will be
terminated and the status set to
`TIMEOUT`.

It is also possible to cancel a job, using the
`cancel` method or the
`cancel_jobs` method. If the job
is currently pending this will set the job status to
`CANCELED`. If the job is
currently running, the job status will be set to
`CANCEL`, and the scheduler will
then attempt to cancel the job. Once the execution has been signaled to
cancel, the job status will change to
`CANCELING`. If the job is
successfully canceled before it otherwise completes, the status will
then change to `CANCELED`.
Otherwise, it will be set to one of the other appropriate final status
values.

Sometimes a job will fail due to transient internal issues, such as the
preemption of the execution resources. In such cases, the job will be
automatically retried. The number of retries is controlled by the
`retry_count` attribute. If a job
fails after all retries have been exhausted, the job status will be set
to `FAILURE`.

Jobs which have completed unsuccessfully (i.e. failed, timed out, or
canceled) can be resubmitted using the
`rerun` method. This will reset
the specified jobs to pending status, and the lifecycle begins over
again. There is no limit to how many times a job can be rerun. Obviously
there is little point in rerunning a job which is failing due to a bug
in the code, but it can be useful in cases where the failure is due to
transient issues, such as rate limits.

Any job which is not currently running can be deleted using its
`delete` method. The
`delete_jobs` method can be used
to delete multiple jobs at once. Once deleted, the job will no longer be
visible in the Compute UI. Running jobs cannot be deleted, but can be
canceled as described above.

#### Job Results

Jobs may either be executed for their side effects (uploading an image
to the Catalog), or for their return value. Return values are
constrained to be serializable: either a `bytes` object, an object which
implements the `Serializable` interface, or
a JSON-serializable object such as a string, number, list, or
dictionary. If the entrypoint function returns a value which does not
meet these criteria, the job will fail. Note in particular that
`Serializable` objects can only be used at the top level; a dictionary
of `Serializable` objects is not itself `Serializable` (although it is
possible implement a mapping type which is `Serializable`).

The return value of a job is available through the
`result` method. This method will
return a `None` if either the job has not (yet) completed successfully,
or if the job did not return a value (e.g. the entrypoint function
either has no `return` statement, or explicitly returns a `None`).
Otherwise it will attempt to deserialize the return value and return it.
In order to deserialize a `Serializable`, you will need to provide a
`cast_type` parameter to the `result`
method so that it knows what type you are trying to deserialize.
Otherwise it will attempt to deserialize the return value as a JSON
object or, failing that, will simply return the raw `bytes` value.

Here is an example of how use the
`Serializable` interface to manage Numpy
arrays as return values:

``` python
import io

import numpy as np

from earthdaily.earthone.compute import Function, Serializable

class SerializableArray(Serializable):
    def __init__(self, value: np.ndarray):
        self.value = value

    def serialize(self):
        memfile = io.BytesIO()
        numpy.save(memfile, self.value)
        return memfile.getvalue()

    @classmethod
    def deserialize(cls, value):
        memfile = io.BytesIO(value)
        memfile.seek(0)
        return cls(numpy.load(memfile))

def hello(i):
    return SerializableArray(np.array([i, i + 1, i + 2]))

job = async_func(5)
job.wait_for_completion()
print(job.result(cast_type=SerializableArray))
```

It is also possible to collect the results for multiple jobs using one
of several Function methods.
`results` will return a list of
results for all jobs which have completed successfully, and
`iter_results` will iterate over
the same but scales better for very large numbers of jobs. It is also
possible to iterate over the results using
`as_completed` as described above.

Non-null results are stored as Catalog Storage Blobs with
`storage_type=StorageType.COMPUTE`, and can also be retrieved directly
using the [Catalog API](catalog.md). This is important
because such blobs can live indefinitely, even after the job and
function have been deleted. Because Storage Blobs can be shared, this
allows you to share your results with others, which isn't possible with
the Compute API.

One important difference when using the Catalog API is that the return
value is not automatically deserialized. Instead, the various methods to
retrieve the blob data will return the raw `bytes`, and you will need to
perform appropriate deserialization explicitly.

In order to leverage the use of storage blobs, which offer many
attributes associated with a data value (such as a geometry, a
description, tags, an expiration date, etc.), the Compute API provides a
special type for annotating return values with these additional
attributes. The `ComputeResult` class can
be used to wrap the return value from the entrypoint function and
associate these additional attributes with it.

``` python
from earthdaily.earthone.compute import Function, ComputeResult

def hello(i):
    return ComputeResult("hello {}".format(i), tags=["hello"])

async_func = Function(
    hello,
    name="my-compute-hello",
    image="python3.10:latest",
    cpus=0.25,
    memory=512,
    maximum_concurrency=1,
    timeout=600,
    retry_count=0,
)
async_func.save()

job = async_func(5)
job.wait_for_completion()
blob = job.result_blob()
print(blob.data())
print(blob.tags)
```

Naturally, all the power of the Catalog can be used for searching and
filtering results. For example, consider an entrypoint function that
operates over a list of tiles or images, and returns `ComputeResult`
objects with the value being some statistic calculated over the tile or
image and with the `geometry` attribute set to the tile or image
geometry. You could then perform a Catalog search for results which
intersect a given geometry:

``` python
from earthdaily.earthone.catalog import Blob, StorageType, properties

search = Blob.search().filter(
    properties.storage_type == StorageType.COMPUTE
).filter(
    properties.namespace == Blob.namespace_id()
).filter(
    properties.name.prefix(f"{async_func.id}/"),
).intersects(
    aoi
)

for blob in search:
    print(result.data())
    print(result.geometry)
```

#### Job Logs

Once a job has completed, successfully or not, logs from the execution
can be retrieved using the `log`
method. This will return a string containing any output to stdout or
stderr (e.g. logging, `print()` statements, etc.) from the execution.
This can be useful for debugging purposes.

As with job results, job logs are stored as Catalog Storage Blobs, and
can be retrieved directly using using the Catalog API. However, unlike
job results, job logs are only stored for 30 days and then are
automatically deleted. They are also deleted when the job or function is
deleted. For this reason, information which needs to be preserved
indefinitely should not be logged, but rather should be stored as (part
of) a job result. Consider using the `extra_properties` attribute of
`ComputeResult` to store such information.

#### Job Statistics

When a job completes (whether with `SUCCESS`, `FAILURE`, or `TIMEOUT`
status), it will be updated with statistics about resource usage for the
job in the `statistics` field. This
includes Cpu, Memory, and Network usage. These values can be useful for
fine-tuning resource requirements for the `Function`. If the resource
requirements for the `Function` are too low, some jobs may fail when
they exceed the limits. On the other hand, if the resource requirements
are too high, you will incur costs for those unused cycles and bytes.

A general rule of thumb is that the resource requirements should be set
to values at least as large as you expect your largest jobs to require.
Then run some representative jobs and examine the statistics to to
determine if the requirements are too high or too low. If your jobs are
failing due to exceeding the memory limit (OOM), you'll need to increase
the requested memory until you can get a clean run. Once you are
satisfied with the maximal requirements of your largest jobs, you can
reduce the requirements to "shrink wrap" the jobs and reduce costs.

#### Job Searches

As with Functions, Jobs can be searched for using the
`search` method. This method returns a
`JobSearch` instance which can be used to
specify additional filtering and sorting criteria. Ultimately, the
search can be executed using the the search in an iteratable context, or
by calling the `count` or
`collect` methods.

Since typically one is interested in the jobs pertaining to a particular
function, the `jobs` property can
be used to create a search for the jobs belonging to the function.

Several Function methods such as
`cancel_jobs` and
`delete_jobs` accept an optional
`JobSearch` instance which will limit the operation to the jobs matching
the search criteria. This can be used, for example, to delete all
canceled jobs:

``` python
async_func.delete_jobs(async_func.jobs.filter(Job.status == JobStatus.CANCELED))
```

## Advanced Compute Usage

Advanced features of Compute allow you to

> - organize your code using standard Python package and module
>   conventions instead of writing all of your code inside a single
>   function
> - add Python dependencies and specify particular version requirements
> - include data files that your function requires to run

We recommend that you use these features to improve the readability of
your code and better control the environment your code executes on.

### Python Package Example

This example shows all the features you can use when using Python
packages to organize your code.

See `scripts/complete_example.py`.

``` python
from earthdaily.earthone.compute import Function

print("creating function")
async_func = Function(
    "compute_examples.complete.simplify",
    name="my-complete-compute-example",
    image="python3.10:latest",
    cpus=0.25,
    memory=512,
    maximum_concurrency=1,
    timeout=600,
    retry_count=0,
    requirements=[
        "geopandas",
    ],
    include_modules=[
        "compute_examples",
    ],
    include_data=[
        "compute_examples/data/*.json"
    ],
)
async_func.save()

# invoking the function
print("submitting a job")
job = async_func(5)

# print the job result and logs
print("waiting for the job to complete")
job.wait_for_completion()
print(job.result())
print(job.log())
```

Instead of defining our function in the deployment script, we've
organized our code using common Python conventions. We've created a
`compute_examples.complete` module which contains the `simplify`
function. Additionally, we tell the Function to include this package,
some additional data, and specific Python requirements for it to run
successfully.

**Including local packages (include_modules).** Your entrypoint function
can make use of any local modules and packages. Specify them by the name
you would use to import them. This includes cython module source files
(with some restrictions, see the section on [Cython
Code](#cython-code)). In this example the assumption is that there is a
local directory `compute_examples` with a `complete.py` file that
defines a `simplify` function. All submodules of the `compute_examples`
package will be included.

**Making Python dependencies available to your code (requirements).**
Your entrypoint function and included modules can make use of any
external Python dependencies that you specify as requirements. In this
example, we specify `geopandas` as a dependency. As long as you pick an
image with your desired Python version (Python 3.10 in this case), you
can upgrade or downgrade any of your other package dependencies as
needed.

**Including data files (include_data).** You can include local data
files that your entrypoint function and included modules can read.
Wildcard patterns such as the `*` (asterisk) - meaning any string - are
supported. Your code must use the `pkg_resources` API to read data files
(see below).

### Code Organization

We suggest that you use customary ways of organizing the code for a
Python project. A common way to organize your source repository looks
like this:

    myproject/
    ├── my_package/
    |   ├── data/
    |   |   └── my_data.txt
    |   ├── __init__.py
    |   ├── models.py
    |   └── utils.py
    |   └── cython_module.pyx
    ├── scripts/
    |   └── deploy_function.py
    └── requirements.txt

- The project's Python code is all contained within a package called
  `my_package`.
- Data is co-located with code within `my_package` so it can be
  referenced relative to the source code.
- A requirements file at the top level lists all the dependencies for
  the the source code. The same requirements file can be given when
  creating a Function.
- A `deploy_function.py` script creates a new Function and kicks off
  jobs. It contains an entrypoint function (see below) which imports
  code from `my_package` to use.

This example follows some general guidelines. But you are not restricted
to a single package and you can organize your code in any way you want,
as long as you can put it together as a list of module names importable
in your current local Python environment.

### Entrypoint Function

You can specify an entrypoint function two ways. As a referenced
function:

``` python
from earthdaily.earthone.compute import Function

def f(x):
    from my_package import my_entrypoint

    return my_entrypoint(x)

async_func = Function(
    f,
    name='hello-world',
    image="python3.10:latest",
    include_modules=[
        'my_package',
    ],
    cpus=0.25,
    memory=512,
    maximum_concurrency=1,
    timeout=600,
    retry_count=0,
)
```

Alternatively, you can use a fully-qualified function name:

``` python
from earthdaily.earthone.compute import Function

async_func = Function(
    'my_package.my_entrypoint',
    name='hello-world',
    image="python3.10:latest",
    include_modules=[
        'my_package',
    ],
    cpus=0.25,
    memory=512,
    maximum_concurrency=1,
    timeout=600,
    retry_count=0,
)
```

Some restrictions apply to one or both methods of passing an entrypoint
function:

- **\*function references only\*** The function needs to be completely
  self-contained. Globals (variables defined in the top-level module
  namespace) cannot be referenced. Define any variables and constants
  within the function's local scope. All modules it uses need to be
  imported within the function. The function can't be decorated. The
  source of the function needs to be available to Compute. This means
  that the function needs to have been loaded from a file, or directly
  in an interpreter such as iPython or a Jupyter notebook which treats
  its input as a source file.
- **\*fully-qualified function name\*** Any modules referenced in your
  packages and submodules need to be locally importable.
- You can only return `bytes`, `Serializable`, or JSON-serializable
  values from the function. If a function returns a value that cannot be
  JSON-serialized, your jobs will fail.
- You can only pass JSON-serializable arguments to the function, e.g.
  arguments with type `str`, `dict`, `list`, `None`, or any numeric data
  type.

### Python Dependencies

You can specify your Python dependencies in two ways. You can give a
list of dependencies:

``` python
from earthdaily.earthone.compute import Function

async_func = Function(
    requirements=[
        "scikit-image==0.13.1".
        "scipy>=1.0.0",
    ],
    ...
)
```

If you already have your dependencies in a standard requirements file
you can give a path (absolute or relative to the current working
directory) to that:

``` python
from earthdaily.earthone.compute import Function

async_func = Function(
    requirements="path/to/requirements.txt",
    ...
)
```

The dependency specification and requirements file use the same format
you are used to from standard Python packaging tools such as pip. For
exhaustive details on this see [PEP 508 for dependency
specification](https://www.python.org/dev/peps/pep-0508/) and the [pip
documentation on requirements
files](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format).

If you specify a different version for a requirement that already exists
on the image, your specified version will take precedence over the
existing version, allowing you to upgrade or downgrade dependencies as
required.

### Cython Code

Cython extension modules can be included in your code in much the same
way as regular Python modules. See
`compute_examples/scripts/cython_example.py`. The source files (.pyx)
will be compiled into extension modules (.so) during the build phase.
However, there are a few restrictions:

- Source cython files in the working directory (where the deploy script
  is being run from) cannot be included. Instead, simply create a
  subdirectory e.g. `my_package` and import the cython module as
  `my_package.cython_module` as in the examples.
- Compute cannot directly execute a function from within a cython module
  as the [Entrypoint Function](#entrypoint-function). Instead of
  executing `cython_example.fib`, create a wrapper function in the
  deployment script that imports and executes `cython_example.fib`. Use
  the wrapper function as the entrypoint.
- `numpy.get_include()` will be added to
  the cythonize's `include_dirs` argument
  to allow the compiler to find numpy header and library files. If you
  request a specific version of numpy in Function
  `requirements` while using numpy in a
  cython module, the job may fail.

> - Cython modules will be compiled using the default settings (except
>   for adding numpy include dirs, discussed above). [Cython compiler
>   options](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-options)
>   are not currently supported.

### Build Failures

If you give Python dependencies for your Function, they are essentially
installed with pip from PyPI into your image before a Function is run.
There is a chance that this dependency build fails. Here are a few
reasons why it might fail:

- You have a typo in your list of requirements and the package doesn't
  exist
- A package version you request is not compatible with the environment
  (e.g. incompatible Python version)
- A package needs system libraries or tools to build that are not
  present in the environment
- The package fails to download from PyPI because of a transient network
  problem
- Data or code files you included are too large

If a problem occurs during the build, the Function will be in a "build
failed" state and not accept jobs anymore.

### Data Files

You can specify data files to be included as a list of patterns:

``` python
from earthdaily.earthone.compute import Function

 async_func = Function(
     include_data=[
         'my_package/data/*.txt',
         'my_package/data/image??.png',
         'my_package/data/document.rst',
     ],
     ...
 )
```

This supports Unix-style pattern expansion as per the [glob
module](https://docs.python.org/2/library/glob.html) in the Python
standard library.

In your code you must read data files using the standard `pkg_resources`
API - not by looking for and opening files directly:

``` python
import pkg_resources
import my_package

# Read a file as a string
text = pkg_resources.resource_string(my_package.__name__, "data/data.txt")

# Open a file as a file-like object
file_like = pkg_resources.resource_stream(my_package.__name__, "data/data.txt")
```

We reference data files relative to the package they are contained in.
For example, the original inclusion path for the file referenced here
would have been `my_package/data/data.txt` - in the package
`my_package`. Colocate your data with your code in a package as much as
possible.

The `pkg_resources` API is part of setuptools, read [more details about
it](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access)
in its documentation.

### Environment Variables

It is possible to set environment variables for your Function and Jobs.
These variables will be defined in the environment of your jobs when
they are running. The
`environment` attribute is a
dictionary of environment variable names and values that will be applied
to all jobs as they are scheduled for execution. The
`environment` attribute is a dictionary
of environment variable names and values that will be merged with the
Function's environment variables for that specific Job. If a variable of
the same name is defined in both the Function and the Job, the Job's
value will take precedence.

It is possible to change the environment variables of a Function or job
after it has been created. However, as the environment variables are
applied to the job when it is scheduled, any changes will only affect
jobs that are scheduled after the change is made. Jobs that are already
running will not be affected.

## Compute Best Practices

**Make the Function idempotent and deterministic**

The Compute service guarantees that every submitted job will run at
least once. Because jobs run on scalable cloud infrastructure it is
possible for a job to be preempted occasionally - this means a job can
forcibly abort at any point in time. If this happens, it will be
restarted from the beginning.

From this follows that the compute function should be idempotent and
(usually) deterministic: if it's aborted at any point and restarted it
should still work and it should produce the same result for the same
input. If a job is long-running and produces an intermediate result
(which is for example persisted to the storage service) it's a good
practice to check for the presence of the intermediate result before
expensively producing it again, and to avoid errors which might arise
when trying to overwrite the result. This saves time in case the
previous run for the same input was preempted.

**Make a job a moderate unit of work**

There is an overhead associated with the startup cost for each job
instance, and there is always a risk that a long running job may be
terminated prematurely due to preemption. There are limits on how many
jobs for each function and for each user may be run concurrently. For
these reasons, it is important to design your jobs to be a moderate unit
of work. A good rule of thumb is that each job should ideally require
between 1 and 10 minutes to complete.

The code in the function itself may have a high startup cost. A typical
example is a function that needs to download a Tensorflow model over the
network and load it into memory. In this case there may be a balance to
strike between many jobs, each of which has the same model loading
overhead, and fewer jobs that run several independent inputs against the
Tensorflow model, amortizing some of the model loading cost. The right
balance depends on your constraints on total runtime and cost.

**Use job results**

Each job produces a result when it completes. The result includes the
return value of the compute function, any output written by the code to
stdout/stderr, and - in case of a failure - details about raised
exceptions. Results for a Function are persisted and can be queried
through the Compute API, as well as browsed in the [Compute
UI](https://earthone.earthdaily.com/compute).

Typically the outcome of a job is some new piece of data such as
metrics, a classification or a geometry. If that data needs to be
persisted and is easily JSON-serializable the simplest solution is to
return it from the compute function as the result.
`iter_results` can then iterate
over all results for a function, and
`result` retrieves individual results
by job. See `retries-reruns-results` for example code. Job results are
stored in the Catalog Storage Blob service, and remain accessible even
when a Function or Job is deleted.

**Use retries and reruns to handle failures**

If a function is doing anything that may occasionally fail by raising an
exception, for example network requests through the Raster API, it's
often a good idea *not* to do explicit error handling. Instead, a
Function can handle occasional failures by giving a `retry_count` during
Function creation (i.e., `Function`); if
any uncaught exceptions are raised during the execution of a function it
is retried this many times before it is finally considered a failure.
This works particularly well if jobs are small, idempotent units of work
as recommended above.

As an alternative or in addition to retries, a set of jobs can also be
rerun through the client. `rerun`
reruns all jobs in a function that have failed. See
`retries-reruns-results` for example code.

## More Examples

### Multiple Jobs Example

This example illustrates the more typical use case of submitting
multiple jobs to a new function.

See `scripts/multiple_jobs.py`

``` python
print("creating function")
async_func = Function(
    "compute_examples.basic.generate_random_image",
    name="my-compute-random-image",
    image="python3.10:latest",
    include_modules=["compute_examples"],
    requirements=[
        "geopandas",
    ],
    cpus=1,
    memory=2048,
    maximum_concurrency=20,
    timeout=600,
    retry_count=1,
)
async_func.save()

print("waiting for function to build")
async_func.wait_for_completion()

# submit 20 jobs to the function
print("submitting jobs")
jobs = async_func.map((i,) for i in range(20))

# wait for jobs, handling each as it completes
for job in async_func.as_completed(jobs):
    if job.status == JobStatus.SUCCESS:
        print(np.array(job.result()).shape)
    else:
        print(job.status)
        print(job.error_reason)
        print(job.log())
```

Here, we reference the `"compute_examples.basic.generate_random_image"`
function which generates a random image using numpy with the same number
of bands as the value passed to the `num_bands` parameter.

This example highlights a few additional features of the Compute API:

- To submit jobs to the Function, we are using the
  `map` method to submit a job for
  each of the elements in the list. This is typically the most efficient
  way to submit jobs to a Function, particularly if the number of jobs
  is large. You are also able to submit jobs one at a time, e.g. within
  in a for-loop.
- We use the `as__completed`
  method to retrieve the results for each job as it is completed. Within
  this loop, we also catch exceptions and print the logs of any failed
  job.

It's important to note that the numpy array return value from the
entrypoint function is converted to a `list` because return values
**must** be JSON-serializable.

### Retries, reruns and job results

This examples demonstrates how to use retries and reruns to make compute
more robust and how to make use of job results.

This is a function that takes a single EarthOne tile as input and
returns a histogram of the pixel values of the NIR band of a Sentinel-2
mosaic around July 2022:

``` python
def nir_histogram(tile):
    from earthdaily.earthone.catalog import *
    from earthdaily.earthone.catalog import properties as p
    import numpy as np

    image_collection = (
        Product.get("esa:sentinel-2:l1c:v1").images()
        .intersects(tile)
        .filter(p.cloud_fraction < 0.2)
        .filter("2022-07-01" <= p.acquired < "2022-01-01")
        .sort("acquired")
        .limit(10)
    ).collect()

    tile_mosaic = image_collection.mosaic("nir", resolution=120)
    histogram, _ = np.histogram(
        tile_mosaic,
        bins=100,
        range=(0, 10000),
        density=False,
    )
    return histogram.tolist()
```

Each histogram is an array of 100 elements corresponding to pixel counts
in 100 bins, evenly spaced from pixel values 0 to 10000. For example,
the first bin is the total number of pixels in a tile that have values 0
to 100.

We can create a Function from this function and run it with tiles
covering the state of New Mexico:

``` python
from earthdaily.earthone.compute import Compute
from earthdaily.earthone.geo import DLTile

async_func = Function(
    nir_histogram,
    name="nir-histogram",
    image="python3.10:latest",
    cpus=1,
    memory=2048,
    maximum_concurrency=20,
    timeout=600,
    retry_count=3,
)
async_func.save()

nm_geom = {
     "type": "Polygon",
     "coordinates": [[
         [-109.039306640625, 37.00255267215955], [-109.039306640625, 31.3348710339506],
         [-108.21533203125, 31.344254455668054], [-108.19335937499999, 31.784216884487385],
         [-106.490478515625, 31.784216884487385], [-106.490478515625, 31.99875937194732],
         [-103.062744140625, 31.99875937194732], [-102.996826171875, 37.00255267215955],
         [-109.039306640625, 37.00255267215955]
     ]]
}
resolution = 10
tile_size = 2000
padding = 0
tiles = DLTile.from_shape(nm_geom, resolution, tile_size, padding)

async_func.map((tile,) for tile in tiles)
async_func.wait_for_completion()
```

Segmenting a large geographic area into tiles and processing one tile
per job like this is a common pattern to parallelize work. This will
kick off and wait for the completion of 867 jobs, each computing a
histogram for one 2000x2000 pixel tile at full resolution of the
Sentinel-2 NIR band (10m per pixel).

When creating the Function, we passed an argument `retry_count=3`. The
`nir_histogram` function uses a raster call - there's a small chance
that this will raise an exception, e.g., because of network instability
or exceeded rate/quota limits. Rather than doing explicit error handling
in the function, we can rely on the retry feature of Compute. If a job
raises an exception here it is retried 3 times before it is discarded as
a failure. Using retries instead of explicit error handling is
recommended if job runtimes are reasonably short.

In the very unlikely case that some jobs failed even with retries, there
is a quick way to rerun all failed jobs:

``` python
async_func.rerun()
async_func.wait_for_completion()
```

`rerun` requires a reference to
the Function. In this case we take it from the previously created
Function.

In other cases we might look up the function id in the [Compute
UI](https://earthone.earthdaily.com/compute), then retrieve the function
by id.

``` python
from earthdaily.earthone.compute import Function
async_func = Function.get("<function-id>")
async_func.rerun()
async_func.wait_for_completion()
```

We broke up our geographic area into tiles so we can run a computation
on high-resolution imagery without running into memory limits and to
speed it up through parallelization. In the end we are after the
aggregate computation across the whole area of the state of New Mexico.
We returned the histograms for each tile from the function, so they are
now stored as job results. We can retrieve and aggregate them:

``` python
import json
import numpy as np
import requests

success_results = async_func.iter_results()
aggregated_histogram = np.zeros((100,))
for result in success_results:
    histogram_list = result
    aggregated_histogram += np.asarray(histogram_list)
```

`iter_results` iterates over all
successfully completed jobs for a Function.

`aggregated_histogram` is now a numpy histogram across the whole state
of New Mexico. This shows how it is often natural to rely on the results
if indeed the return value of the function is the crucial outcome of a
job - as opposed to other cases where the return value is insignificant
because the side effect of the job matters, such as typically the upload
of a new raster scene into the catalog.

### File storage

You can use the directory located at `/tmp` for file storage while your
job is running. This directory is an ephemeral filesystem and is a good
place to write temporary files during the run of a single job. There is
approximately 16GB of space available. All files will be deleted when
the job completes.

See `scripts/cache_example.py`

``` python
from earthdaily.earthone.compute import Function

def hello(i):
    from compute_examples.cache import hello

    # specify a file location in the cache to write files to
    return hello(i, "/tmp/geometry.wkt")

print("creating function")
async_func = Function(
    hello,
    name='my-compute-hello',
    image="python3.10:latest",
    include_modules=[
        "compute_examples"
    ],
    cpus=1,
    memory=2048,
    maximum_concurrency=1,
    timeout=600,
    retry_count=3,
)
async_func.save()

# submit a job to the function
print("submitting a job")
job = async_func(5)

# print the job result and logs
print("waiting for the job to complete")
job.wait_for_completion()
print(job.result())
print(job.log())
```

## Choosing Your Environment

The execution environment for your function in the cloud is defined by
the docker image you pick when creating the function. The below images
are available covering typical use cases.

Match your local Python version to the image you choose. Your function
will be rejected or might not run successfully if there is a mismatch
between your local Python version and the Python version in the image. A
differing bug release version (the "x" in Python version "3.10.x") is
fine.

### Current Images

**Python 3.14, latest**  
Image: `python3.14:latest`\
Date: 02/17/2026\
Python highlights: GDAL, numpy, rasterio\
Other libraries and tools: proj 9.1.1, GDAL 3.6.2

``` none
affine==2.4.0
annotated-types==0.7.0
attrs==25.4.0
blosc2==4.0.0
cachetools==7.0.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
cligj==0.7.2
dill==0.4.1
dynaconf==3.2.12
earthdaily==1.10.0
earthdaily-earthone==6.0.1
GDAL==3.6.2
geojson==3.2.0
geopandas==1.1.2
idna==3.11
imagecodecs==2026.1.14
lazy-object-proxy==1.12.0
mercantile==1.2.1
msgpack==1.1.2
ndindex==1.10.1
numexpr==2.14.1
numpy==2.4.2
packaging==26.0
pandas==3.0.1
pillow==12.1.1
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.2
python-dateutil==2.9.0.post0
rasterio==1.5.0
requests==2.32.5
shapely==2.1.2
six==1.17.0
StrEnum==0.4.15
tifffile==2026.2.16
toml==0.10.2
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
```


**Python 3.13, latest**  
Image: `python3.13:latest`\
Date: 02/17/2026\
Python highlights: GDAL, numpy, rasterio\
Other libraries and tools: proj 9.1.1, GDAL 3.6.2

``` none
affine==2.4.0
annotated-types==0.7.0
attrs==25.4.0
blosc2==4.0.0
cachetools==7.0.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
cligj==0.7.2
dill==0.4.1
dynaconf==3.2.12
earthdaily==1.10.0
earthdaily-earthone==6.0.1
GDAL==3.6.2
geojson==3.2.0
geopandas==1.1.2
idna==3.11
imagecodecs==2026.1.14
lazy-object-proxy==1.12.0
mercantile==1.2.1
msgpack==1.1.2
ndindex==1.10.1
numexpr==2.14.1
numpy==2.4.2
packaging==26.0
pandas==3.0.1
pillow==12.1.1
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.2
python-dateutil==2.9.0.post0
rasterio==1.5.0
requests==2.32.5
shapely==2.1.2
six==1.17.0
StrEnum==0.4.15
tifffile==2026.2.16
toml==0.10.2
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
```


**Python 3.12, latest**  
Image: `python3.12:latest`\
Date: 02/17/2026\
Python highlights: GDAL, numpy, rasterio\
Other libraries and tools: proj 9.1.1, GDAL 3.6.2

``` none
affine==2.4.0
annotated-types==0.7.0
attrs==25.4.0
blosc2==4.0.0
cachetools==7.0.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
cligj==0.7.2
dill==0.4.1
dynaconf==3.2.12
earthdaily==1.10.0
earthdaily-earthone==6.0.1
GDAL==3.6.2
geojson==3.2.0
geopandas==1.1.2
idna==3.11
imagecodecs==2026.1.14
lazy-object-proxy==1.12.0
mercantile==1.2.1
msgpack==1.1.2
ndindex==1.10.1
numexpr==2.14.1
numpy==2.4.2
packaging==26.0
pandas==3.0.1
pillow==12.1.1
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.2
python-dateutil==2.9.0.post0
rasterio==1.5.0
requests==2.32.5
shapely==2.1.2
six==1.17.0
StrEnum==0.4.15
tifffile==2026.2.16
toml==0.10.2
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
```

**Python 3.11, latest**  
Image: `python3.11:latest`\
Date: 02/17/2026\
Python highlights: GDAL, numpy, rasterio\
Other libraries and tools: proj 9.1.1, GDAL 3.6.2

``` none
affine==2.4.0
annotated-types==0.7.0
attrs==25.4.0
blosc2==4.0.0
cachetools==7.0.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
click-plugins==1.1.1.2
cligj==0.7.2
dill==0.4.1
dynaconf==3.2.12
earthdaily==1.10.0
earthdaily-earthone==6.0.1
GDAL==3.6.2
geojson==3.2.0
geopandas==1.1.2
idna==3.11
imagecodecs==2026.1.14
lazy-object-proxy==1.12.0
mercantile==1.2.1
msgpack==1.1.2
ndindex==1.10.1
numexpr==2.14.1
numpy==2.4.2
packaging==26.0
pandas==3.0.1
pillow==12.1.1
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.2
python-dateutil==2.9.0.post0
rasterio==1.4.4
requests==2.32.5
shapely==2.1.2
six==1.17.0
StrEnum==0.4.15
tifffile==2026.2.16
toml==0.10.2
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
```

**Python 3.10, latest**  
Image: `python3.10:latest`\
Date: 02/17/2026\
Python highlights: GDAL, numpy, rasterio\
Other libraries and tools: proj 9.1.1, GDAL 3.6.2

``` none
affine==2.4.0
annotated-types==0.7.0
attrs==25.4.0
blosc2==4.0.0
cachetools==7.0.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
click-plugins==1.1.1.2
cligj==0.7.2
dill==0.4.1
dynaconf==3.2.12
earthdaily==1.10.0
earthdaily-earthone==6.0.1
GDAL==3.6.2
geojson==3.2.0
geopandas==1.1.2
idna==3.11
imagecodecs==2025.3.30
lazy-object-proxy==1.12.0
mercantile==1.2.1
msgpack==1.1.2
ndindex==1.10.1
numexpr==2.14.1
numpy==2.2.6
packaging==26.0
pandas==2.3.3
pillow==12.1.1
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.1
python-dateutil==2.9.0.post0
pytz==2025.2
rasterio==1.4.4
requests==2.32.5
shapely==2.1.2
six==1.17.0
StrEnum==0.4.15
tifffile==2025.5.10
toml==0.10.2
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.3
urllib3==2.6.3
```

