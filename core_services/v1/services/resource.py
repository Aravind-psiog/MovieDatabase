import os


def resources():
    """
    Resources
    ----------------

    This function will return a set of resources to handle API Gateway routing

    Args: None

    Returns: A set of resources for API Gateway routes handling
    """
    resource_path = {
        "staging": os.environ.get("stage_path"),
        "resource": os.environ.get("resource_path"),
    }
    return resource_path
