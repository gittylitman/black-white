# FROM python:3.11

# # ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
# # RUN sh /home/netfree-unix-ca.sh
# # ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
# # ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
# # ENV SSL_CERT_FILE=/etc/ca-bundle.crt


# RUN apt-get update && \
#     apt-get install -y curl apt-transport-https gnupg && \
#     echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | \
#     tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
#     curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
#     apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
#     apt-get update && \
#     apt-get install -y google-cloud-sdk

# WORKDIR /app

# COPY ./ /app


# RUN pip install .

# CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]

FROM python:3.11-slim

# התקנות בסיסיות
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://sdk.cloud.google.com | bash && \
    apt-get clean

ENV PATH="/root/google-cloud-sdk/bin:${PATH}"

# התקנת flet
RUN pip install flet

WORKDIR /app
COPY main.py .

EXPOSE 8550
CMD ["python", "src/main.py"]
