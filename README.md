# WhatsApp Message Sender

Sistema para envio de mensagens WhatsApp em lote usando Twilio, com integração ao Slack para notificações e monitoramento.

## 🚀 Funcionalidades

- Envio de mensagens WhatsApp em lote
- Processamento em lotes com delay configurável
- Barra de progresso visual
- Integração com Slack para notificações
- Estatísticas detalhadas de execução
- Tratamento de erros robusto
- Logs formatados

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Google Cloud Platform
- Conta no Twilio
- Webhook do Slack
- Acesso ao BigQuery

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd task-twilio-send-whatsapp
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Configure as credenciais do Google Cloud:
```bash
# Instale o Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Faça login
gcloud auth login

# Configure o projeto
gcloud config set project [SEU_PROJETO_ID]

# Configure as credenciais de aplicativo
gcloud auth application-default login
```

2. Crie um arquivo `.env` na raiz do projeto:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/SEU/WEBHOOK/URL
```

## 🚀 Execução

Para executar o script:
```bash
python main.py
```

## 📊 Estrutura do Projeto

```
.
├── src/
│   ├── config/         # Configurações
│   ├── models/         # Modelos de dados
│   ├── services/       # Serviços
│   └── utils/          # Utilitários
├── main.py            # Ponto de entrada
├── queries.py         # Queries do BigQuery
├── twilio_service.py  # Serviço do Twilio
└── requirements.txt   # Dependências
```

## 🔄 Deploy no Google Cloud

1. Crie um arquivo `app.yaml`:
```yaml
runtime: python39
entrypoint: python main.py

env_variables:
  SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/SEU/WEBHOOK/URL"
```

2. Faça o deploy:
```bash
gcloud app deploy
```

## 📝 Logs e Monitoramento

- Logs são exibidos no console com timestamp e nível
- Resumo detalhado é enviado para o Slack
- Estatísticas incluem:
  - Total de usuários
  - Mensagens enviadas/falhas
  - Taxa de sucesso
  - Tempo de execução
  - Erros detalhados

## 🔍 Troubleshooting

1. Erro de autenticação do Google Cloud:
```bash
gcloud auth application-default login
```

2. Erro de permissão no BigQuery:
- Verifique se a conta de serviço tem as permissões necessárias
- Verifique se o projeto está corretamente configurado

3. Erro no envio de mensagens:
- Verifique as credenciais do Twilio
- Verifique o formato dos números de telefone

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
