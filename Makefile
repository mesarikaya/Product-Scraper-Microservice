GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create djangowebproductscraper\
		--scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform"

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
	gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/djangowebscraper .

.PHONY: push
push: build
	gcloud docker push -- gcr.io/$(GCLOUD_PROJECT)/djangowebscraper

.PHONY: template
template:
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" djangowebscraper.yaml

.PHONY: deploy
deploy: push template
	kubectl create -f djangowebscraper.yaml

.PHONY: update
update:
	kubectl patch deployment djangowebscraper -p "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"`date +'%s'`\"}}}}}"

.PHONY: delete
delete:
	kubectl delete rc djangowebscraper
	kubectl delete service djangowebscraper
