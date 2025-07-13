FROM python:3.12.2
WORKDIR /app

COPY ./ /app

RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://sdk.cloud.google.com | bash && \
    apt-get clean

ENV PATH="/root/google-cloud-sdk/bin:${PATH}"
RUN pip install  .
CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]