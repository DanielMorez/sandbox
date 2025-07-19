from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    k8s_namespace: str = "sandbox"
    job_ttl_seconds: int = 60
    max_active_jobs: int = 1

    cpu_limit: str = "200m"
    memory_limit: str = "128Mi"
    kubeconfig: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=(".env",),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


settings = Settings()
