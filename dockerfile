FROM python:3.12.2

WORKDIR /app

COPY ./ /app

RUN pip install -r requirement.txt

CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]