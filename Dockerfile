FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/projects/reportify
RUN chmod -R 777 /opt/projects/reportify

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /opt/projects/reportify
WORKDIR /opt/projects/reportify

RUN mkdir -p static/
RUN mkdir -p staticfiles/

CMD python manage.py migrate && \
    python manage.py collectstatic
