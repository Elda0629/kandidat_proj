PYTHON ?= python3.12
VENV_DIR ?= .venv
PIP := $(VENV_DIR)/bin/pip

.PHONY: venv install clean activate run fuzzy
	
run: 
	python3 checklist_chatbot.py

graph:
	python3 chatbot-graph.py

fuzzy:
	python3 fuzzy_search.py

venv:
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

install: venv

clean:
	@rm -rf $(VENV_DIR)

activate: venv
	@echo "Starting zsh with virtual environment activated..."
	@zsh -c 'zsh -c "source ~/.zshrc 2>/dev/null || true; source $(VENV_DIR)/bin/activate; echo \"Virtual environment is now active!\"; exec zsh"'