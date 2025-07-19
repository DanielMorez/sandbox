from jinja2 import Template
from sandbox_core.language_registry import LANGUAGE_REGISTRY

def generate_job_yaml(language: str, code_b64: str, job_name: str, memory: str, cpu: str) -> str:
    config = LANGUAGE_REGISTRY[language]
    with open(f'k8s/templates/{config["template"]}') as f:
        template = Template(f.read())
    return template.render(
        job_name=job_name,
        code_b64=code_b64,
        image=config["image"],
        filename=config["filename"],
        run_cmd=config["run_cmd"],
        memory=memory,
        cpu=cpu,
    )
