FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD ["uvicorn", "bet_maker.application:app", "--host", "0.0.0.0"]
