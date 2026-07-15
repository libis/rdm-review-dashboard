# Author: Eryk Kulikowski @ KU Leuven (2023). Apache 2.0 License

STAGE ?= prod

include env.$(STAGE)
export

.SILENT:
SHELL = /bin/bash

# Set USER_ID and GROUP_ID to current user's uid and gid if not set
USER_ID ?= $(shell id -u)
GROUP_ID ?= $(shell id -g)

.PHONY: build-frontend
build-frontend: 
	echo "Building frontend ..."
	cd ./rdm-review-dashboard-ui && npm install &&  rm -rf ./dist && npx ng build --configuration="production" --base-href $(BASE_HREF)

.PHONY: build-check
build-check: 
	echo "Building check-my-dataset ui ..."
	cd ./rdm-check-my-dataset && npm install && rm -rf ./dist && npx ng build --configuration="production" --base-href $(BASE_HREF_CHECK)

# `build` is the cross-repo contract target — rdm-deployment's initialize.mak
# builds every sibling repo with `make build STAGE=…`.
.PHONY: build
build: build-image

build-image: build-frontend build-check
	echo "Building Docker image ..."
	rm -rf rdm-review-dashboard-backend/image/dist
	rm -rf rdm-review-dashboard-backend/image/src
	cp -r rdm-review-dashboard-ui/dist rdm-review-dashboard-backend/image/dist
	cp -r rdm-check-my-dataset/dist rdm-review-dashboard-backend/image/
	cp rdm-review-dashboard-backend/requirements.txt rdm-review-dashboard-backend/image/
	cp -r rdm-review-dashboard-backend/src rdm-review-dashboard-backend/image/src
	docker build \
		--build-arg USER_ID=$(USER_ID) --build-arg GROUP_ID=$(GROUP_ID) \
		--tag "$(IMAGE_TAG)" ./rdm-review-dashboard-backend/image

run: venv 
	. ./rdm-review-dashboard-backend/.venv/bin/activate && cd ./rdm-review-dashboard-backend/src && uvicorn main:api --proxy-headers --host 0.0.0.0 --port 8000 --workers 4

autocheck-consumer:
	cd ./rdm-review-dashboard-backend/src && huey_consumer.py autochecks.autocheck_tasks.huey  -f --workers 1

.PHONY: venv
venv: 
	python3 -m venv ./rdm-review-dashboard-backend/.venv
	. ./rdm-review-dashboard-backend/.venv/bin/activate && python -m pip install --upgrade pip && pip install -r ./rdm-review-dashboard-backend/requirements.txt

.PHONY: test
test: venv
	. .venv/bin/activate \
		&& python -m pip install -r rdm-review-dashboard-backend/requirements.txt -r rdm-review-dashboard-backend/requirements-dev.txt \
		&& python -m pytest -q rdm-review-dashboard-backend/tests

push: 
	if [ "$(STAGE)" = "prod" ]; then \
		echo "Pushing Docker image to repository ..."; \
		docker push $(IMAGE_TAG); \
	else \
		echo "Not in production stage. Pushing not allowed."; \
	fi