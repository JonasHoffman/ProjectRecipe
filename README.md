Recipe AI

Backend de uma aplicação de receitas com Inteligência Artificial, busca por ingredientes, processamento de linguagem natural e interação por mensagens de texto ou áudio.

O projeto foi inicialmente idealizado para funcionar como um assistente de receitas através do WhatsApp. A ideia era permitir que o usuário enviasse uma mensagem como:

"Quero uma receita com frango e creme de leite."

ou até mesmo um áudio:

"Quero uma receita fácil com chocolate."

A aplicação interpreta a intenção do usuário, consulta uma base de receitas e retorna sugestões relevantes.

Durante o desenvolvimento, o Telegram foi utilizado como canal de integração, permitindo implementar e testar o fluxo de mensagens e áudio sem depender da infraestrutura da API oficial do WhatsApp.

Sobre o projeto

O Recipe AI foi desenvolvido como um projeto de estudo e portfólio com foco em backend, integração de APIs, processamento de dados e Inteligência Artificial.

A aplicação reúne diferentes componentes:

Coleta de receitas de sites públicos
Normalização dos dados coletados
Persistência em PostgreSQL
Busca por ingredientes
Busca utilizando linguagem natural
Interpretação de mensagens com Gemini
Recomendação de receitas
Processamento de mensagens de voz com Whisper
Integração com Telegram
API REST com FastAPI

A arquitetura foi pensada de forma que o canal de comunicação possa ser substituído no futuro. Dessa forma, a integração atual com Telegram pode evoluir para uma integração com WhatsApp sem precisar alterar a lógica principal da aplicação.

Fluxo da aplicação

O fluxo principal pensado para o projeto é:

                    ┌─────────────────┐
                    │     Usuário     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Canal de entrada│
                    │ WhatsApp* /     │
                    │ Telegram        │
                    └────────┬────────┘
                             │
                     Texto ou áudio
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌──────────────┐          ┌──────────────┐
        │    Texto     │          │    Whisper   │
        │              │          │    (áudio)   │
        └──────┬───────┘          └──────┬───────┘
               │                         │
               └────────────┬────────────┘
                            ▼
                    ┌─────────────────┐
                    │     Gemini      │
                    │ Interpretação   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Busca / seleção │
                    │    de receitas  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Receita /       │
                    │ recomendação    │
                    └─────────────────┘

* WhatsApp representa o canal originalmente planejado. A integração implementada atualmente utiliza Telegram.

Funcionalidades
Busca por ingredientes

É possível procurar receitas utilizando ingredientes disponíveis.

Exemplo:

cenoura

A aplicação consulta as receitas armazenadas e retorna os resultados correspondentes.

Busca em linguagem natural

O usuário pode escrever uma solicitação mais natural, por exemplo:

Quero uma receita fácil com frango e creme de leite.

O Gemini interpreta a mensagem e transforma a solicitação em parâmetros estruturados para a busca.

Isso permite separar a interpretação da linguagem natural da lógica responsável por consultar o banco de dados.

Recomendação de receitas

O projeto também possui uma camada de recomendação utilizando Inteligência Artificial.

A ideia é permitir que o sistema analise o contexto da solicitação do usuário e selecione receitas mais adequadas.

Mensagens de áudio

O projeto utiliza Whisper localmente para transformar mensagens de voz em texto.

Fluxo:

Mensagem de voz
       ↓
Telegram
       ↓
Download do arquivo de áudio
       ↓
Whisper
       ↓
Texto transcrito
       ↓
Gemini
       ↓
Busca / recomendação

Isso permite que o usuário interaja com o sistema sem precisar digitar a solicitação.

Integração com Telegram

Durante o desenvolvimento, o Telegram foi utilizado como canal de comunicação para validar o fluxo que originalmente foi pensado para WhatsApp.

O webhook recebe as atualizações enviadas pelo Telegram e diferencia mensagens de texto e mensagens de voz.

A camada de integração está separada da lógica principal da aplicação para facilitar a substituição ou adição de outros canais no futuro.

Coleta de receitas

As receitas são coletadas de diferentes fontes através de parsers específicos.

Atualmente existem parsers para:

TudoGostoso
Panelinha
Receiteria

O projeto possui uma camada comum para os scrapers, permitindo que cada fonte tenha sua própria implementação sem misturar regras específicas de cada site.

Fluxo:

Site
 ↓
HTTP Client
 ↓
Parser específico
 ↓
Dados brutos
 ↓
Normalizer
 ↓
Modelo da aplicação
 ↓
PostgreSQL
Normalização

Como cada site possui uma estrutura HTML e uma forma diferente de representar as receitas, os dados coletados passam por uma etapa de normalização.

O RecipeNormalizer transforma diferentes formatos de entrada em uma estrutura comum utilizada pela aplicação.

Por exemplo, informações como:

nome da receita
tempo de preparo
quantidade de porções
ingredientes
quantidade dos ingredientes
unidade de medida
modo de preparo
imagem
fonte

são convertidas para um formato consistente.

Isso permite que a aplicação trabalhe com receitas provenientes de diferentes sites sem precisar conhecer a estrutura original de cada fonte.

Banco de dados

O projeto utiliza PostgreSQL para armazenar as receitas e seus ingredientes.

A estrutura possui, entre outros, os seguintes conceitos:

Recipe
   │
   └── RecipeIngredient
             │
             └── Ingredient

Um ingrediente pode estar relacionado a diversas receitas, enquanto uma receita pode possuir diversos ingredientes.

As alterações da estrutura do banco são controladas utilizando Alembic.

Inteligência Artificial

O projeto utiliza a API do Google Gemini para tarefas relacionadas à interpretação e recomendação.

Um dos principais usos é transformar uma solicitação em linguagem natural em uma estrutura que possa ser utilizada pela aplicação.

Exemplo conceitual:

"Quero uma receita rápida com frango e pouca coisa."

                    ↓

{
    "ingredients": ["frango"],
    "max_preparation_time": ...,
    "preferences": [...]
}

A aplicação então utiliza essas informações para realizar a busca.

Essa separação evita colocar a lógica de consulta ao banco diretamente dentro do prompt da IA.

Processamento de áudio

Para reconhecimento de voz foi escolhido o Whisper, executado localmente.

A implementação está concentrada em:

app/audio/transcriber.py

A classe SpeechToText é responsável por carregar o modelo e realizar a transcrição.

O uso de Whisper local também permite manter o reconhecimento de voz independente de um serviço externo específico.

API

A aplicação utiliza FastAPI para disponibilizar os endpoints.

Entre os fluxos implementados estão:

GET /recipes

Busca receitas utilizando ingredientes.

GET /recipes/natural-search

Busca utilizando linguagem natural.

GET /recipes/{recipe_id}

Retorna os detalhes de uma receita.

O FastAPI também fornece a documentação interativa através de:

/docs
Estrutura do projeto

A estrutura principal da aplicação é:

ProjectRecipe/
│
├── app/
│   ├── ai/
│   │   ├── client.py
│   │   ├── recommender.py
│   │   └── selector.py
│   │
│   ├── audio/
│   │   └── transcriber.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── integrations/
│   │   └── telegram/
│   │       ├── bot.py
│   │       └── client.py
│   │
│   ├── models/
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   └── recipe_ingredient.py
│   │
│   ├── normalizer/
│   │   └── recipe.py
│   │
│   ├── persistence/
│   │   └── recipe.py
│   │
│   ├── schemas/
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   └── telegram.py
│   │
│   ├── scraper/
│   │   ├── base.py
│   │   ├── http_client.py
│   │   ├── resolver.py
│   │   │
│   │   ├── panelinha/
│   │   │   └── parser.py
│   │   │
│   │   ├── receitaria/
│   │   │   └── parser.py
│   │   │
│   │   └── tudogostoso/
│   │       └── parser.py
│   │
│   ├── search/
│   │   ├── interpreter.py
│   │   ├── recipe.py
│   │   └── service.py
│   │
│   └── main.py
│
├── alembic/
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Os diretórios __pycache__ foram omitidos por serem arquivos gerados automaticamente pelo Python.

Tecnologias
Backend
Python
FastAPI
Pydantic
SQLAlchemy
Alembic
PostgreSQL
Inteligência Artificial
Google Gemini API
Whisper
Web scraping
HTTPX
BeautifulSoup
Integrações
Telegram Bot API
ngrok durante o desenvolvimento local
Desenvolvimento
Git
GitHub
Virtual Environment
Configuração

Crie um arquivo .env na raiz do projeto.

Exemplo:

DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=recipe_ai

GEMINI_API_KEY=sua_chave_gemini

TELEGRAM_BOT_TOKEN=seu_token_telegram

NUM_PROJETO=seu_numero_do_projeto

O arquivo .env não deve ser versionado.

Utilize o .env.example como referência para configurar o ambiente.

Instalação

Clone o repositório:

git clone https://github.com/JonasHoffman/ProjectRecipe.git
Entre no projeto:

cd ProjectRecipe

Crie o ambiente virtual:

python -m venv venv

Ative o ambiente virtual no Windows:

.\venv\Scripts\Activate.ps1

Instale as dependências:

pip install -r requirements.txt

Configure o arquivo .env e crie o banco PostgreSQL.

Depois execute as migrations:

alembic upgrade head
Executando a aplicação

Com o ambiente virtual ativado:

uvicorn app.main:app --reload

A API ficará disponível localmente em:

http://localhost:8000

A documentação interativa pode ser acessada em:

http://localhost:8000/docs
Telegram e webhook

Para testar a integração com Telegram durante o desenvolvimento local, o projeto utiliza um túnel público apontando para a aplicação FastAPI.

Exemplo:

Telegram
    ↓
Webhook público
    ↓
ngrok
    ↓
localhost:8000
    ↓
FastAPI

Essa abordagem permite testar o webhook localmente sem precisar hospedar a aplicação durante o desenvolvimento.

Testes

O projeto possui testes e scripts de validação para diferentes componentes, incluindo:

conexão com PostgreSQL
interpretação de buscas com Gemini
transcrição de áudio com Whisper
parsers de receitas
normalização dos dados
fluxo de integração com Telegram

Durante o desenvolvimento, os componentes também foram validados individualmente antes de serem integrados ao fluxo principal.

Estado atual

O projeto possui um fluxo funcional de:

Telegram
   ↓
FastAPI
   ↓
Texto / Áudio
   ↓
Whisper
   ↓
Gemini
   ↓
Busca / recomendação
   ↓
PostgreSQL
   ↓
Receita

Atualmente a base de dados possui receitas coletadas de diferentes fontes e a aplicação consegue trabalhar com busca por ingredientes, linguagem natural e mensagens de voz.

A integração com Telegram foi utilizada como implementação prática do conceito originalmente pensado para WhatsApp.

Próximos passos

Algumas evoluções possíveis para o projeto são:

integração oficial com WhatsApp
melhorar o sistema de recomendação
melhorar o tratamento de erros da IA
adicionar mais fontes de receitas
melhorar a seleção de receitas por contexto
adicionar autenticação de usuários
criar histórico de buscas e preferências
adicionar testes automatizados de integração
disponibilizar a aplicação em ambiente de produção
Objetivo do projeto

O principal objetivo do Recipe AI é explorar, em um único projeto, diferentes conceitos importantes do desenvolvimento backend moderno:

construção de APIs
modelagem de banco de dados
migrations
web scraping
normalização de dados
processamento de linguagem natural
Inteligência Artificial
reconhecimento de voz
integração com APIs externas
arquitetura modular
testes
desenvolvimento orientado a um fluxo real de usuário

O projeto também foi pensado como uma base para futuramente transformar o assistente em uma aplicação acessível diretamente por canais de mensagens, começando pelo conceito de WhatsApp e utilizando Telegram como ambiente de implementação e testes.