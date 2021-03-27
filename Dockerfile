FROM python:3.6
WORKDIR /src
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod -R 777 .
COPY src .
ENTRYPOINT ["python","main.py"]