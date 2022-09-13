FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./comspacity_frontend.py /code/

EXPOSE 8501

CMD ["streamlit", "run", "comspacity_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]