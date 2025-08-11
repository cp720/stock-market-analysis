FROM apache/airflow:2.9.1-python3.11


USER root
WORKDIR /opt/airflow

# Bring in project code and set ownership
COPY src/ /opt/airflow/src/
RUN chown -R airflow:0 /opt/airflow/src

# Copy requirements
COPY requirements.txt /tmp/requirements.txt

# Switch to airflow
USER airflow

# Install Python deps as airflow user
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# Keep PYTHONPATH
ENV PYTHONPATH=/opt/airflow/src
