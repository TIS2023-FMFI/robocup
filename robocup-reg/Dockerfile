FROM python:3.10.13-slim-bullseye

WORKDIR /app
RUN useradd --create-home appuser \
    && chmod 777 /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

RUN pip install --upgrade pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY --chown=appuser:appuser . /app/
USER root
RUN chmod -R 777 /app/
USER appuser
CMD ["/app/entrypoint.sh"]
