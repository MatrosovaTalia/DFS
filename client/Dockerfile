FROM python:3.7-alpine
WORKDIR /client
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY ./ /client


#CMD python3 /client/client.py
CMD ["python3","-u","/client/client.py"]