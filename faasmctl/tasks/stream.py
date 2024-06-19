from base64 import b64encode
from faasmctl.util.invoke import invoke_wasm
from faasmctl.util.planner import (
    get_available_hosts,
    reset_batch_size,
    scale_function_parallelism,
    reset_max_replicas,
    reset_stream_parameter,
)
from faasmctl.util.results import (
    get_execution_time_from_message_results,
    get_return_code_from_message_results,
)
from invoke import task
from sys import exit
from time import time


@task(default=True)
def scale(
    ctx,
    user,
    function,
    parallelism,
    ini_file=None,
):
    """
    Change the parallelism of a function
    """
    req_dict = {"user": user, "function": function, "parallelism": parallelism}

    if user is None or function is None or parallelism is None:
        print("ERROR: user, function and parallelism must be provided")
        return 1
    
    req_dict["user"] = user
    req_dict["function"] = function
    req_dict["parallelism"] = int(parallelism)
    scale_function_parallelism(user, function, parallelism)

@task
def batch(ctx, batchsize):
    """
    Reset the batch size
    """
    reset_batch_size(batchsize)

@task
def replica(ctx, max_replicas):
    """
    Reset the maximum number of replicas
    """
    reset_max_replicas(max_replicas)

@task
def reset(ctx, parameter, value):
    """
    Reset a STREAM parameter
    """
    reset_stream_parameter(parameter, value)