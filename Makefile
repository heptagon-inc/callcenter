.DEFAULT_GOAL := help

## Deploy
deploy:
	credentor -- yarn sls deploy -v -s ${STAGE}

## Encrypt credential file
encrypt:
	openssl enc -e -aes-256-cbc -salt \
		-k ${ENCRYPT_PASS} \
		-in credentials.json \
		-out credentials.json.enc

## Decrypt credential file
decrypt:
	openssl enc -d -aes-256-cbc -salt \
		-k ${ENCRYPT_PASS} \
		-in credentials.json.enc \
		-out credentials.json

## Show help
help:
	@make2help $(MAKEFILE_LIST)

.PHONY: help
.SILENT:
