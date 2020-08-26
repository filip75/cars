# Cars


### Setup for development
In directory where docker-compose.yaml is create two files with following values:

django.env:
* SECRET_KEY=\<scret_key\>
* DEBUG=true
* ALLOWED_HOSTS=\<List of allowed hosts sparated by comas. Most likely just localhost.\>
* DJANGO_SETTINGS_MODULE=cars.settings.prod

postgres.env:
* POSTGRES_USER=\<user name\>
* POSTGRES_PASSWORD=\<password\>
* POSTGRES_DB=\<name of database\>
* POSTGRES_DB_HOST=cars_db
* POSTGRES_DB_PORT=5432

Than run `make run`

## Running tests
After application has been build run `make test`

## Deployment

Application is deployed here

https://cars12345678.herokuapp.com/cars/

https://cars12345678.herokuapp.com/rate/

https://cars12345678.herokuapp.com/top/



## Dependecies
* databse - postgres
* application server in production - gunicron 
