 FROM django:1.10-python2
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 RUN pip install mongoengine==0.8.0
 ADD ./UIOP /code/
 EXPOSE 8000
 EXPOSE 28017
 CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
 RUN /usr/local/mongodb/bin/mongo
