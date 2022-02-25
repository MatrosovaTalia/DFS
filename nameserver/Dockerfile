FROM python:3.7-alpine
WORKDIR /nameserver
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY ./ /nameserver


#CMD python3 /nameserver/ne_name_server.py
CMD ["python3","-u","/nameserver/name_server.py"]