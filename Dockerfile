FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install Flask

RUN pip install flask_sqlalchemy

RUN pip install flask_wtf

ENV FLASK_APP=website

COPY website ./website

COPY comparative_judgements.db .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]