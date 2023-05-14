FROM python:3.11-slim

RUN useradd appuser

WORKDIR /home/appuser

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install gevent

COPY app app
COPY start.py config.py boot.sh .env ./
RUN mkdir instance
RUN chmod +x boot.sh

RUN chown -R appuser:appuser ./
USER appuser

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]