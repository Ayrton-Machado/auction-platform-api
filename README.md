# auction-platform-api

![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

> API completa para sistema de leilões online com **autenticação JWT, criação de anúncios, sistema de lances, watchlist e comentários**. 
> Suporta **categorias, administração via Django Admin e controle de leilões ativos/fechados**.

### Ajustes e melhorias
O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- [ ] Atualizar retorno de todos os endpoints.
- [ ] Acrescentar testes em todo o projeto.
- [ ] Integrar Postgres.
- [ ] Implementar autenticação JWT.

**IA de Confiança:**
- [ ] Criar repositório separado no Hugging Face Hub.
- [ ] Desenvolver modelo de análise de imagem no Jupyter.
- [ ] Treinar modelo NLP para análise de descrições.
- [ ] Publicar modelo treinado no Hugging Face Hub.
- [ ] Integrar API do Hugging Face no endpoint de confiança.

**Deploy e Infraestrutura:**
- [ ] Configurar Droplet para backend Django.
- [ ] Configurar PostgreSQL Managed Database.
- [ ] Implementar DigitalOcean Spaces para upload de imagens.
- [ ] Deploy do frontend no App Platform.
- [ ] Configurar domínio customizado e SSL.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou a versão mais recente do [Python 3.13+](https://www.python.org/)

## 🚀 Instalando

Para instalar, siga estas etapas:

1. Clone o repositório:
```bash
git clone https://github.com/Ayrton-Machado/auction-platform-api
cd auction-platform-api
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o setup do Banco de Dados:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. (Opcional) Criar superuser para acessar Django Admin:
```bash
python manage.py createsuperuser
```
- http://127.0.0.1:8000/api/admin

## ☕ Usando

Para usar, siga estas etapas:

1. Iniciar API
```
python manage.py runserver
```

2. Acesse a documentação API Swagger.
- http://127.0.0.1:8000/api/docs


## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.