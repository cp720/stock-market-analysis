# infrastructure/airflow/Dockerfile
FROM apache/airflow:2.9.1-python3.11

USER root
WORKDIR /opt/airflow

# Copy and install pinned dependencies
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Bring in project code
COPY src/ /opt/airflow/src/

# Give airflow user ownership of code tree
RUN chown -R airflow /opt/airflow/src

USER airflow

# Ensure package is on the Python path so imports like
# `from stock_market_analysis.pipeline import ...` work
ENV PYTHONPATH=/opt/airflow/src
