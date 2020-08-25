build:
	docker-compose build

heroku_push:
	cd ./cars && heroku container:push --app cars12345678 web

heroku_release:
	heroku container:release web --app cars12345678

heroku_restart:
	heroku restart --app cars12345678

run:
	docker-compose up -d

test:
	docker run \
	--entrypoint /code/manage.py \
	--env-file django.env \
	--env-file postgres.env \
	-e DJANGO_SETTINGS_MODULE=cars.settings.test \
	-v $(shell pwd)/cars:/code \
	cars_web \
	test 


