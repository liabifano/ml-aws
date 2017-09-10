FROM python:3

EXPOSE 8080

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel
RUN python3 -m pip install virtualenv==15.1.0

COPY modelapp/ /modelapp/
COPY VERSION VERSION

# create virtualenv
RUN bash /modelapp/bootstrap-python-env.sh

# run tests
RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf && \
    . /modelapp-python-env/bin/activate && \
    cd modelapp/ && py.test

# run application
CMD . modelapp-python-env/bin/activate && \
    python3 modelapp/src/modelapp/manage.py runserver --host 0.0.0.0  --port=8080
