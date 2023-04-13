FROM python:3.11-bullseye

EXPOSE 80

USER 0

# Install python requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app files
RUN mkdir /app
WORKDIR /app
COPY . .

# Run server
CMD [ "python", "app/manage.py", "runserver", "0.0.0.0:80" ]