.PHONY: dev serve install

install:
	pip install mkdocs-material mkdocs-encryptcontent-plugin

serve:
	mkdocs serve

dev: _fetch-private serve

_fetch-private:
	@echo "→ Fetching private documentation content..."
	@./scripts/fetch-private-content.sh
	@echo "→ Private content ready. Starting server...\n"
