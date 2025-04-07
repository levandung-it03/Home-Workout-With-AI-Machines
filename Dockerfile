
FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install fastapi[standard]


COPY ./app /code/app
COPY ./.env /code/.env


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "60"]