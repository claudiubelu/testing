FROM python:3.8-alpine

# Create and change the working directory to /sobolanism.
WORKDIR /sobolanism

# Add the project inside the image.
ADD . .

# Install the project requirements.
RUN pip install -r requirements.txt
ENV PYTHONPATH /sobolanism

# Set an entrypoint which will execute when starting this image.
# The arguments we can accept in our microservice can be passed as the
# container's command, leaving the entrypoint unchanged.
ENTRYPOINT ["python3", "sobolanism/cmd/worker.py"]
