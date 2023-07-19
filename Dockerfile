FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder

EXPOSE 8000

WORKDIR /voi

COPY requirements.txt /voi

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./voi /voi

WORKDIR /voi

ENTRYPOINT ["python3"] 

# Start should be with Gunicorn
CMD ["manage.py", "runserver", "0.0.0.0:8000"]