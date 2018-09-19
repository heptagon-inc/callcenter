.DEFAULT_GOAL := help

## Deploy
deploy:
	credentor -- yarn sls deploy -v -s ${STAGE}

## Show help
help:
	@make2help $(MAKEFILE_LIST)

.PHONY: help
.SILENT:
