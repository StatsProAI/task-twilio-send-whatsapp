.PHONY: install run clean build push deploy

# Variáveis do Google Cloud
PROJECT_ID=auroraaidev
REGION=us-central1
REPOSITORY=statspro-whatsapp
IMAGE_NAME=statspro-whatsapp

# Comando para instalar as dependências
install:
	pip3 install -r requirements.txt

# Comando para executar a aplicação
run:
	python3 main.py

# Comando para limpar arquivos temporários
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Comando para fazer build da imagem Docker
build:
	docker build -t $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):latest .

# Comando para fazer push da imagem para o Google Cloud
push:
	gcloud auth configure-docker $(REGION)-docker.pkg.dev
	docker push $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):latest

# Comando para build e push em sequência
deploy: build push 