FROM python:3
COPY ./todoapp/ /opt/
WORKDIR /opt/
RUN pip install -r requirements.txt && python manage.py migrate && python manage.py makemigrations todo && python manage.py migrate todo && python manage.py migrate todo.tests
EXPOSE 8000
ENTRYPOINT python manage.py runserver 0.0.0.0:8000 --insecure
