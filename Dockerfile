FROM python:3.11-alpine

WORKDIR /app


COPY ./gaming-app.py /app
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN addgroup -S gaming-app && adduser -S gaming-app -G gaming-app
USER gaming-app

ENTRYPOINT ["python", "gaming-app.py"]
