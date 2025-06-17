# 📱 iPhone Price Tracker – Web Scraping no Mercado Livre

Pipeline de **Web Scraping + PostgreSQL + Telegram Bot** para monitoramento de preços de iPhones no Mercado Livre. O sistema coleta os dados da página do produto, armazena no banco de dados e envia **notificações automáticas** no Telegram sempre que um novo *maior preço* é identificado.

---

## 📚 Visão Geral

- **Coleta:** Extrai nome do produto e preços (antigo, atual e parcelado) via scraping do Mercado Livre.
- **Armazenamento:** Salva os dados em um banco de dados PostgreSQL.
- **Notificação:** Envia alerta via Telegram sempre que um novo maior preço é detectado.

---

## 🗂️ Estrutura do Projeto

```bash
iphone_price_tracker/
├── iphone_scraping.py       # Script principal (scraping + DB + Telegram)
├── Dockerfile               # Imagem Docker customizada
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente (NÃO subir ao Git)
└── README.md
```

---

## ⚙️ Configuração do Ambiente

### 1. **Pré-requisitos**

- [Docker](https://www.docker.com/)
- Conta no Telegram e criação de um bot ([veja como criar um bot aqui](https://core.telegram.org/bots#6-botfather))
- Banco de dados PostgreSQL acessível

### 2. **Clone o Repositório**

```bash

https://github.com/vbluuiza/iphone-web-scraping-project
cd iphone-web-scraping-project
```

### 3. **Crie o Arquivo `.env`**

Baseie-se no modelo abaixo:

```
TELEGRAM_TOKEN=seu_token_do_bot
TELEGRAM_CHAT_ID=seu_chat_id

POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=host_do_postgres
POSTGRES_PORT=porta_do_postgres
```

---

## 🐳 Execução com Docker

### 1. **Construa a Imagem Docker**

```bash
docker build -t iphone-scraping .
```

### 2. **Execute o Container**

```bash
docker run --env-file .env iphone-scraping
```

📌 *Certifique-se de que o banco PostgreSQL esteja acessível ao container.*

---

## 🧩 Personalização

Para alterar o produto monitorado:

- Edite a URL diretamente na função `fetch_page()` do arquivo `iphone_scraping.py`.

---

## 📝 Observações

- O banco de dados deve conter uma tabela para armazenar os dados. Ela será criada automaticamente se não existir.

---

## 📌 Referência

Este projeto foi inspirado em um conteúdo do canal [**Jornada de Dados**](https://www.youtube.com/@JornadaDeDados), adaptado e expandido para fins de aprendizado.

---

## 👩‍💻 Desenvolvido por

Luiza Vieira – Estudante de Análise e Desenvolvimento de Sistemas - Cesar School

- 💼 [LinkedIn](https://www.linkedin.com/in/vbluuiza)
- 💻 [GitHub](https://github.com/vbluuiza)