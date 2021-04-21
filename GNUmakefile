NAME=vagrant
BINARY=packer-plugin-${NAME}

COUNT?=1
TEST?=$(shell go list ./...)

.PHONY: dev generate

build:
	@go build -o ${BINARY}

dev: build
	@mkdir -p ~/.packer.d/plugins/
	@mv ${BINARY} ~/.packer.d/plugins/${BINARY}

run-example: dev
	@packer build ./example

test:
	@go test -count $(COUNT) $(TEST) -timeout=3m

testacc: dev
	@PACKER_ACC=1 go test -count $(COUNT) -v $(TEST) -timeout=120m

install-gen-deps: ## Install dependencies for code generation
	@go install github.com/hashicorp/packer-plugin-sdk/cmd/packer-sdc

generate: ## install-gen-deps
	@echo "==> removing autogenerated markdown..."
	@find docs-partials/ -type f | xargs grep -l '^<!-- Code generated' | xargs rm -f
	@echo "==> removing autogenerated code..."
	@find ./ -type f | xargs grep -l '^// Code generated' | xargs rm -f
	PROJECT_ROOT="$(CURDIR)" go generate ./...
	## Takes generated partials and renders single markdown files.
	packer-sdc renderdocs -src content-files/docs -partials docs-partials -dst docs/

ci-release-docs:
	@go install github.com/hashicorp/packer-plugin-sdk/cmd/packer-sdc@latest
	@packer-sdc renderdocs -src docs -partials docs-partials/ -dst docs/
	@/bin/sh -c "[ -d docs ] && zip -r docs.zip docs/"