FROM python:3.9

WORKDIR app

COPY pyproject.toml poetry.lock server.py ./
COPY mic_racoon_challange ./mic_racoon_challange
COPY dist ./dist
RUN touch README.md

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "-u", "server.py"]