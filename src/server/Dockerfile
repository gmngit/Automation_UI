FROM python:3.12-alpine

FROM python:3.12-alpine

LABEL description="server"

WORKDIR /exam_app

ADD ./ ./

EXPOSE 8081

RUN pip install --no-cache-dir -e .
RUN ["pip", "install", "--no-cache-dir", "gunicorn"]
ENV FLASK_APP=run.py
RUN flask db upgrade && flask add-user admin@gcore.qa zxcvbn --admin

CMD ["gunicorn", "-b 0.0.0.0:8081",  "run:app"]
