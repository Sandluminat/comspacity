FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./comspacity_backend.py /code/

EXPOSE 8000

CMD ["uvicorn", "comspacity_backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]