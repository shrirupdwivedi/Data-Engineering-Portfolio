# Base Image
FROM python:3.8-slim
LABEL maintainer="Shrirup"

WORKDIR /usr/app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./
CMD ["python", "app.py"]