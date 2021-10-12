FROM python:3.9.7
COPY requirements.txt /src/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r /src/requirements.txt
COPY app/.env /src
COPY app/schedule.py /src
COPY ../../dock_mongo/data/support-eng.json /src/data/support-eng.json
WORKDIR /src
CMD ["venv/bin/python", "schedule.py"]