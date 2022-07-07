FROM python:3.9-slim
RUN apt-get update \
    && apt-get install wget gcc ffmpeg libsm6 libxext6 tesseract-ocr-por -y \
    && apt-get clean \
    && wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb \
    && wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg8-empty/libjpeg8_8c-2ubuntu8_amd64.deb \
    && dpkg -i libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb \
    && dpkg -i libjpeg8_8c-2ubuntu8_amd64.deb \
    && rm -f *.deb \
    && ln -sf /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime \
    && pip install --upgrade pip setuptools wheel

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY /app /app/app
COPY /premier-pet.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

ENV PYTHONPATH=/app

ENTRYPOINT ["python3", "app/src/api/main.py"]
