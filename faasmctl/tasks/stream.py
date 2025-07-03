from base64 import b64encode
from faasmctl.util.invoke import invoke_wasm
from faasmctl.util.planner import (
    get_available_hosts,
    reset_batch_size,
    scale_function_parallelism,
    reset_max_replicas,
    reset_stream_parameter,
    register_function_state,
    custom_request,
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
    initialize=False,
    ini_file=None,
):
    """
    Change the parallelism of a function
    """
    if user is None or function is None or parallelism is None:
        print("ERROR: user, function and parallelism must be provided")
        return 1

    scale_function_parallelism(user, function, parallelism, initialize)

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

@task
def register_state(ctx, function, partitioned_arrtibue = None, state_key = None):
    """
    Register a state for a function
    """
    if function is None:
        print("ERROR: function must be provided")
        return 1
    register_function_state(function, partitioned_arrtibue, state_key)

@task
def custom(ctx, key, value = None):
    custom_request(key, value)