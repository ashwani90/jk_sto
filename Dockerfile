FROM python:3.11.3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install spacy
RUN python -m spacy download en_core_web_sm
RUN pip install -r requirements.txt
RUN pip install psycopg2==2.8.6
COPY . /code/

ENTRYPOINT [ "tail" ]
CMD ["-f", "/dev/null"]