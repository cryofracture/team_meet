FROM python:3.9.7
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY app /src
CMD python /src/schedule.py