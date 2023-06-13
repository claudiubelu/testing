FROM python:3.8-alpine

WORKDIR /sobolanism
ADD . .
RUN pip install -r requirements.txt
ENV PYTHONPATH /sobolanism

ENTRYPOINT ["python3", "sobolanism/cmd/client.py"]
