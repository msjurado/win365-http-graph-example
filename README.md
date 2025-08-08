# win365-http-graph-example
Basic example using http calls to Microsoft graph API for authentication and calling a Windows 365 endpoint.  Example is using registered app in Azure with certificate authentication.

#### Create new conda environment
```bash
conda create --name <env> --file requirements.txt python=3.12
```

#### Create a self signed cert for testing called w365.key and a public cert called w365.pem
```bash
openssl genrsa -des3 -out w365.key 2048
openssl req -new -key w365.key -out w365.csr -sha256
openssl x509 -req -in w365.csr -signkey w365.key -out w365.pem -days 365 -sha256 -extfile w365.conf -extensions v3_req
```

#### Upload your public cert (w365.pem) and note your sha1 thumbprint for use in .env file

#### .env file in root is required to supply sensitive info not stored in repo
```
TENANT_ID=<your azure tenant id>
CLIENT_ID=<client id from app registration>
PRIVATE_KEY=<path to private key file>
PRIVATE_KEY_PASSPHRASE=<passphrase for private key>
CERT_THUMBPRINT=<SHA1 thumbprint provided by Microsoft when public key uploaded to registered app>
```