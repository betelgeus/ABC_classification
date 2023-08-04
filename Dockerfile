FROM python:3

WORKDIR /app

VOLUME ["/app/data"]

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]