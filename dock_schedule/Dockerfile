FROM python:3.9.7
COPY requirements.txt /src/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install flask
RUN pip install python-dotenv
RUN pip install -r /src/requirements.txt
COPY app/.env /src
COPY app/schedule.py /src
COPY mock_data/support-eng.json /src/data/support-eng.json
WORKDIR /src

ENV FLASK_APP=/src/schedule.py:app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]