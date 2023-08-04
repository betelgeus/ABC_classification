run:
	docker run -p 8000:8000 -d --name abc_class -v ABC_IMAGES:/app/data shekhovda/abc_classification:dev

start:
	docker start abc_class


stop:
	docker stop abc_class