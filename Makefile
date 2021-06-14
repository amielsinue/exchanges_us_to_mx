# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

null:
	help

# Makefile Command Line Arguments!
ARGS = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`


.PHONY: dev-install
dev: ## Pip install
	docker-compose up --build app

.PHONY: dev-tests
dev-tests: ## Run unit tests
	docker-compose up --build tests