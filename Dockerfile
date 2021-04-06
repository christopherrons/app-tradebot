FROM python:3.6
WORKDIR /src
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python","main.py"]