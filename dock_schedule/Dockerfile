FROM python:3.9.7
COPY requirements.txt /src/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r /src/requirements.txt
COPY app /src
CMD python /src/schedule.py