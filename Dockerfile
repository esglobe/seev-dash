FROM python:3.10

ENV GITHUB_LINK=https://github.com/esglobe/seev-dash
ENV ESGLONBE_LINK=https://esglobe.github.io/
ENV ISABEL_LINK=https://www.linkedin.com/in/isabel-llatas-b103911/

COPY . /app-run

WORKDIR /app-run

RUN set -ex \
    && pip install --upgrade pip \
    && pip install -r ./requirements.txt

CMD exec gunicorn --conf /app-run/server_conf.py index:server --reload