FROM python:3.12.2

WORKDIR /app

COPY ./ /app

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .

CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]