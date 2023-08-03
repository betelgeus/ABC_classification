FROM python:3

WORKDIR /Users/mitya/PycharmProjects/ABC_detection/

VOLUME ["/Users/mitya/PycharmProjects/ABC_detection/data/uloaded_files/"]

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--port", "8000"]
