import inspect
from datetime import datetime


def get_docstr() -> str:
    # Get the current frame
    current_frame = inspect.currentframe()

    try:
        # Get the calling frame
        calling_frame = current_frame.f_back  # type: ignore

        # Get the actual function object from the calling frame
        current_function = calling_frame.f_globals[calling_frame.f_code.co_name]  # type: ignore

        return current_function.__doc__
    finally:
        # Always remember to explicitly close the frame to avoid leaks
        # (otherwise, it will be kept alive by references)
        del current_frame


def get_name() -> str:
    # Get the current frame
    current_frame = inspect.currentframe()

    try:
        # Get the calling frame
        calling_frame = current_frame.f_back  # type: ignore

        # Get the actual function object from the calling frame
        current_function = calling_frame.f_globals[calling_frame.f_code.co_name]  # type: ignore

        return current_function.__name__
    finally:
        # Always remember to explicitly close the frame to avoid leaks
        # (otherwise, it will be kept alive by references)
        del current_frame


def add_step(json_metadata, description: str, func: callable):
    _add_step_description(json_metadata, description)

    if func is not None:
        func()

    _set_step_outcome(json_metadata, "passed")


def _add_step_description(json_metadata, description: str):
    print('################################################################################')
    print(f'{datetime.now()}: step: {description}')
    print('################################################################################')

    step = {}

    step["description"] = description
    step["outcome"] = "failed"  # Will be overriden when the step is successfully completed

    json_metadata[f'step-{json_metadata["steps"]}'] = step
    json_metadata["steps"] = json_metadata["steps"] + 1


def _set_step_outcome(json_metadata, outcome: str):
    json_metadata[f'step-{json_metadata["steps"] - 1}']['outcome'] = outcome
