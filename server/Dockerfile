FROM python:3.7-alpine
WORKDIR /server
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY ./ /server


#CMD python3 /server/data_server.py
CMD ["python3","-u","/server/data_server.py"]