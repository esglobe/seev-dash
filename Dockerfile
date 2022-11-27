FROM python:3.10

COPY . /app-run

WORKDIR /app-run

RUN set -ex \
    && pip install --upgrade pip \
    && pip install -r ./requirements.txt

#EXPOSE 8000

#ENTRYPOINT gunicorn --conf /app-run/server_conf.py index:server --reload
CMD ["gunicorn", "--conf", "/app-run/server_conf.py", "--reload", "index:server"]