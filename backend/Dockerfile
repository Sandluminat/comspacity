FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./comspacity_backend.py /code/

EXPOSE 8000

# No logs
CMD ["gunicorn", "comspacity_backend:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--reload"]

# logs
# CMD ["gunicorn", "--access-logfile", "-","--error-logfile", "-", "--log-level", "info", "comspacity_backend:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--reload"]