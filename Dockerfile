FROM python:3.10

WORKDIR /app

RUN pip install flask
RUN pip install requests
RUN pip install jwt
RUN pip install flask-cors


# COPY ./requirements.txt requirements.txt



# RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0



EXPOSE 5001


COPY ./requirements.txt ./
COPY ./app.py ./



CMD ["flask", "run", "--port=5001"]


## BUILD:   docker build . -t flask_docker
## DELETE: docker container rm -f flask_docker
## RUN:     docker run -d --name flask_docker -p 5000:5000 --restart=always flask_docker
## first port is host, second port is docker guest (see EXPOSE command)
# docker image prune
# docker container ls