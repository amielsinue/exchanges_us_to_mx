
Requirements
-----------
- Docker Compose
- make
- create .env file from .env.example 
- Register and get a token from fixer https://fixer.io/
- Set that token on the env variables
- Register and get an api_key from  banxico https://www.banxico.org.mx/SieAPIRest/service/v1/doc/consultaDatosSerieRango
- set that api_key on the env variables


Run local
-----------
```bash
make dev
```

Run Tests
-----------
```bash
make dev-tests
```


How to use
-----------

#### Register
```.env
curl --location --request POST 'localhost:5000/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "amielsinue@gmail.com",
    "password": "apostoles"
}'
```
Response:
```.env
{
    "id": 1,
    "email": "amielsinue@gmail.com",
    "api_token": "0315df8ae56228f77964de637659be69"
}
```

#### Login
you have to login whenever the error is expired token
```.env
curl --location --request POST 'localhost:5000/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "amielsinue@gmail.com",
    "password": "apostoles"
}'
```
Response:
```
{
    "id": 1,
    "email": "amielsinue@gmail.com",
    "api_token": "0315df8ae56228f77964de637659be69"
}
```

#### Get exchanges
```.env
curl --location --request GET 'localhost:5000/exchanges' \
--header 'Authorization: Token 69f1a68cd818112c62cb05d0cbdb4a02'
```

