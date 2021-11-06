# FROM ubuntu
# RUN apt-get update -y && apt-get install -y python3-pip python-dev 

# COPY ./requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN pip install -r requirements.txt 
# COPY . /app
# ENTRYPOINT [ "python" ]
# CMD ["lms.py"]

FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000 
CMD ["python", "./lms.py"]