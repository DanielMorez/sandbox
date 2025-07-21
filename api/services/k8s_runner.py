import uuid
import base64
import logging

import yaml
from kubernetes import client, config, watch
from api.config import settings
from k8s.generate_job import generate_job_yaml
from sandbox_core.language_registry import LANGUAGE_REGISTRY

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if settings.debug:
    config.load_kube_config()
else:
    config.load_incluster_config()

batch = client.BatchV1Api()
core = client.CoreV1Api()

async def run_code_in_k8s(request):
    if request.language not in LANGUAGE_REGISTRY:
        raise ValueError(f"Язык {request.language} не поддерживается")

    # Проверка на перегрузку
    jobs = batch.list_namespaced_job(namespace=settings.k8s_namespace)
    active_jobs = sum(1 for job in jobs.items if job.status.active)
    if active_jobs >= settings.max_active_jobs:
        raise RuntimeError("Сервис перегружен. Попробуйте позже.")

    job_name = f"{request.language}-{uuid.uuid4().hex[:8]}"
    code_b64 = base64.b64encode(request.code.encode()).decode()
    yaml_manifest = generate_job_yaml(
        language=request.language,
        code_b64=code_b64,
        job_name=job_name,
        memory=settings.memory_limit,
        cpu=settings.cpu_limit
    )
    yaml_manifest_dict = yaml.safe_load(yaml_manifest)

    job_spec = client.ApiClient()._ApiClient__deserialize(yaml_manifest_dict, client.V1Job)

    # Создание job
    batch.create_namespaced_job(namespace=settings.k8s_namespace, body=job_spec)

    # Ожидание завершения job
    w = watch.Watch()
    try:
        for event in w.stream(batch.list_namespaced_job, namespace=settings.k8s_namespace, timeout_seconds=30):
            job = event["object"]
            if job.metadata.name == job_name:
                if job.status.succeeded:
                    break
                if job.status.failed:
                    raise RuntimeError("Код завершился с ошибкой")
    finally:
        w.stop()

    # Получение pod
    pods = core.list_namespaced_pod(namespace=settings.k8s_namespace, label_selector=f"job-name={job_name}")
    pod_name = pods.items[0].metadata.name

    # Чтение логов
    logs = core.read_namespaced_pod_log(name=pod_name, namespace=settings.k8s_namespace)

    # Удаление Job
    batch.delete_namespaced_job(
        name=job_name,
        namespace=settings.k8s_namespace,
        propagation_policy="Background"
    )

    return {
        "job_name": job_name,
        "status": "success",
        "output": logs
    }
