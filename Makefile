# Author: Eryk Kulikowski @ KU Leuven (2023). Apache 2.0 License

STAGE ?= dev
BASE_HREF ?= /ui/

include .env
-include .env.local
export

.SILENT:
SHELL = /bin/bash

# Set USER_ID and GROUP_ID to current user's uid and gid if not set
USER_ID ?= $(shell id -u)
GROUP_ID ?= $(shell id -g)


build-frontend: ## Build Frontend
	echo "Building frontend ..."
	cd ./rdm-review-dashboard-ui && rm -rf ./dist && npm install && ng build --configuration="production" --base-href $(BASE_HREF)

build-container: build-frontend ## Build Docker image
	echo "Building Docker image ..."
	rm -rf rdm-review-dashboard-backend/image/dist
	rm -rf rdm-review-dashboard-backend/image/src
	cp -r rdm-review-dashboard-ui/dist rdm-review-dashboard-backend/image/dist
	cp rdm-review-dashboard-backend/requirements.txt rdm-review-dashboard-backend/image/
	cp -r rdm-review-dashboard-backend/src rdm-review-dashboard-backend/image/src
	docker build \
		--build-arg USER_ID=$(USER_ID) --build-arg GROUP_ID=$(GROUP_ID) \
		--tag "$(IMAGE_TAG)" ./rdm-review-dashboard-backend/image

run:
	cd ./rdm-review-dashboard-backend/src && uvicorn main:api --proxy-headers --host 0.0.0.0 --port 8000 --workers 4