FROM jupyter/datascience-notebook:latest
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt