FROM python:3.4-alpine
RUN mkdir -p /srv/test_app
ADD . /srv/test_app
WORKDIR /srv/test_app
RUN pip3 install -r requirements.txt
CMD [ "python3", "wsgi.py" ]
