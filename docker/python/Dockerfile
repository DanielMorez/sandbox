FROM python:3.11-slim

# Добавляем пользователя с UID 1000
RUN adduser --uid 1000 --disabled-password --gecos "" sandbox

# Создаем директорию для работы с кодом и даём права
RUN mkdir /workspace && chown sandbox:sandbox /workspace

# Копируем файл запуска
COPY code.py /workspace/
RUN chmod +x /workspace/code.py

# Устанавливаем рабочую директорию и пользователя
USER 1000
WORKDIR /workspace

# Указываем точку входа
ENTRYPOINT ["python", "code.py"]
