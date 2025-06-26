FROM python:3.12.2
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
WORKDIR /app

COPY ./ /app

RUN pip install  .

CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]