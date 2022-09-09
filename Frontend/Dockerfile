FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./comspacity_frontend.py /code/

EXPOSE 10101

CMD ["streamlit", "run", "comspacity_frontend.py"]