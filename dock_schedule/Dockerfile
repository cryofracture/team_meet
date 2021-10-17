# Building from a stable, supported version of Python 3
FROM python:3.9.7

# Requirements are for Flask and Google Calendar Authorization
COPY requirements.txt /src/requirements.txt

# Upgrade pip as container fails - oddity with 3.9.x
RUN /usr/local/bin/python -m pip install --upgrade pip

# flask in the requirements folder was not installing properly. Installed manually here, and same with python-dotenv.
RUN pip install flask
RUN pip install python-dotenv

# Install remaining dependencies
RUN pip install -r /src/requirements.txt

# TODO: investigate cloud-based secrets management so script can make an encrypted API call vs take an env file.
COPY app/.env /src

# TODO: Remove this once mongo server is implemented correctly.
COPY mock_data/support-eng.json /src/mock_data/support-eng.json

# set WORKDIR
WORKDIR /src

# Ensure fastest build time, copying source code as late as possible.
COPY app/schedule.py /src

# enable "flask run" command
ENV FLASK_APP=schedule.py:app

EXPOSE 8080

# start the app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]