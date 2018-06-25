# todoapp
Python Django Todo Application

# Imp Urls:
1. Res.gister url : {host_ip}/portal/register/
2. Login url: {host_ip}/portal/login/
3. Index page: {host_ip}/portal/index/
4. Subtasks and status: {host_ip}/portal/todo-tasks/{tasklist}
5. Get all tasks with subtasks: {host_ip}/portal/todo/ : methods: get(), post()

# Features
1. Create main task
2. Add subtasks
3. Change status of subtasks ("Open", "In-Progress", "Done")
4. Search in main tasks by title

# Deployment
On prem:
1. Create virtual env
2. Clone project in env
3. install requirments.txt
> pip install -r requirements.txt
4. Setup django buildin models
> python manage.py migrate
5. Create tables for application models
> python manage.py makemigrations todo
> python manage.py migrate todo
6. Run server
> python manage.py runserver 0.0.0.0:8000

On Docker:
1. Make sure docker service running
2. build image using Dockerfile provided in project
> docker build -t todoapp .
3. Once image build complete check for the latest build in docker image repo (local). and get image id
> docker images -a
4. Run docker container with image id
> docker run -p {system port : 80}:{exposed port of container: 8000} -itd {image id}
5. Check logs of system:
> docker logs {container id}
