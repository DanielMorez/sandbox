LANGUAGE_REGISTRY = {
    "python": {
        "image": "denisduginov/sandbox-python:latest",
        "template": "python_job.yaml.j2",
        "filename": "code.py",
        "run_cmd": "python code.py"
    },
}
