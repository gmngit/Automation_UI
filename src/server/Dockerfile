FROM python:3.12-alpine

FROM python:3.12-alpine

LABEL description="UI Exam server"

WORKDIR /exam_app

ADD ./ ./

EXPOSE 8081

RUN pip install --no-cache-dir -e .
RUN ["pip", "install", "--no-cache-dir", "gunicorn"]
RUN flask db upgrade && flask add-user admin@gcore.qa zxcvbn --admin

CMD ["gunicorn", "-b 0.0.0.0:8081",  "run:app"]
