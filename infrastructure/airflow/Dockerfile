# infrastructure/airflow/Dockerfile
FROM apache/airflow:2.9.1-python3.11

USER root
WORKDIR /opt/airflow

# Bring in only what's needed for pip install
COPY pyproject.toml README.md /opt/airflow/
COPY src/                       /opt/airflow/src/

# Give the airflow user ownership of the src/ tree
RUN chown -R airflow /opt/airflow/src

USER airflow

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Now install pip & your package in editable mode
RUN pip install --no-cache-dir --upgrade pip \
 && pip install -e ".[airflow]"
