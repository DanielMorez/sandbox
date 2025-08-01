# 🧪 Sandbox Kubernetes Runner

Этот сервис позволяет запускать пользовательский код внутри изолированных Kubernetes Job'ов. Используется в сценариях, где требуется безопасное выполнение произвольного кода (например, обучение, тестовые окружения и т.п.).

---

## 🚀 Алгоритм работы

1. Пользователь отправляет код (например, на Python) через API.
2. Сервис кодирует его в base64 и подставляет в шаблон Kubernetes Job (Jinja2).
3. Kubernetes запускает Job с указанным образом.
4. Внутри контейнера:
   - код сохраняется в файл внутри `emptyDir`-тома;
   - запускается с помощью интерпретатора (например, `python code.py`).
5. После выполнения Job автоматически удаляется (`ttlSecondsAfterFinished`).
6. Результаты исполнения доступны через API (или логирование).

---

## 🧰 Технологический стек

| Компонент        | Версия / Особенности                  |
|------------------|----------------------------------------|
| Python           | >= 3.13                                |
| FastAPI          | Веб-фреймворк для API                  |
| Uvicorn          | ASGI-сервер                            |
| Kubernetes SDK   | Работа с кластером из Python           |
| Jinja2           | Шаблонизация манифестов                |
| Poetry           | Управление зависимостями и билдом      |

---

## ⚙️ Переменные окружения

Все переменные загружаются через `pydantic-settings`.

| Название                    | Описание                                            | Пример                            |
|-----------------------------|-----------------------------------------------------|------------------------------------|
| `KUBERNETES_NAMESPACE`      | Namespace, в котором запускаются Job'ы             | `default`                          |
| `SANDBOX_IMAGE_PYTHON`      | Имя образа для запуска Python-кода                 | `denisduginov/sandbox-python`      |
| `CPU_LIMIT`                 | Ограничение по CPU для job                         | `500m`                             |
| `MEMORY_LIMIT`              | Ограничение по памяти                              | `256Mi`                            |
| `JOB_TTL_SECONDS`           | Через сколько секунд удаляется завершённый Job     | `60`                               |
| `KUBECONFIG` (опционально)  | Путь к kubeconfig, если не в кластере              | `/home/user/.kube/config`          |

---

## 📁 Структура проекта

```text
sandbox/
│
├── api/                          # FastAPI-приложение
│   ├── main.py                   # Точка входа в API
│   ├── routers/                  # Разделенные роуты (run, result и т.п.)
│   │   ├── run.py
│   │   └── result.py
│   ├── services/                 # Логика работы с K8s, очередями
│   │   ├── k8s_runner.py
│   │   └── result_fetcher.py
│   ├── schemas/                  # Pydantic-схемы
│   │   └── run.py
│   └── config.py                 # Настройки проекта (env, paths и т.п.)
│
├── docker/                      # Контейнеры для разных языков
│   ├── python/
│   │   ├── Dockerfile
│   │   └── run_code.py
│   ├── nodejs/
│   │   ├── Dockerfile
│   │   └── run_code.js
│   ├── cpp/
│   │   ├── Dockerfile
│   │   └── run_code.cpp
│   └── java/
│       ├── Dockerfile
│       └── run_code.java
│
├── k8s/                         # K8s-манифесты или генераторы job'ов
│   ├── templates/               # Jinja2-шаблоны для job'ов по языкам
│   │   ├── python_job.yaml.j2
│   │   ├── nodejs_job.yaml.j2
│   │   └── ...
│   └── generate_job.py          # Генератор манифеста job по языку
│
├── sandbox_core/                # Общая логика запуска (может использоваться и worker'ами)
│   ├── language_registry.py     # Реестр поддерживаемых языков
│   ├── executor.py              # Базовая логика сборки job
│   └── validators.py
│
├── scripts/
│   ├── build_images.sh          # CI/CD билдер образов по всем языкам
│   └── cleanup_jobs.py          # Удаление устаревших job'ов
│
├── helm/                        # Helm-чарт для развёртывания API
│   └── sandbox-api/
│       └── ...
│
├── tests/                       # Юнит- и интеграционные тесты
│   └── test_api.py
│
├── poetry.lock                         # Переменные окружения
└── README.md
```