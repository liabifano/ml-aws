FROM python:3.6.2

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel virtualenv==15.1.0

COPY modelapp/ /modelapp/
COPY resources/model/ resources/model/

# create virtualenv
RUN bash /modelapp/bootstrap-python-env.sh

# run unit tests
RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf && \
    . /modelapp-python-env/bin/activate && \
    cd modelapp/ && py.test

# run application
WORKDIR /modelapp/src/modelapp
CMD . ../../../modelapp-python-env/bin/activate && \
    gunicorn --bind 0.0.0.0:8080 -k eventlet manage:app
