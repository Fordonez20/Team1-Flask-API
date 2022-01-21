FROM python:3.8-slim-buster

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY application.py application.py
ENV FLASK_APP=application.py

EXPOSE 5000

CMD ["python3", "application.py"]