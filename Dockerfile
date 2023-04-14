FROM python:3.11-bullseye

EXPOSE 80

USER 0

# Install python requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app files
RUN mkdir /app
WORKDIR /app
COPY ./app/. ./docker-entrypoint.sh .

# Create dir for static files
RUN mkdir -p /data/staticfiles

# Run entrypoint script
ENTRYPOINT [ "bash", "./docker-entrypoint.sh" ]