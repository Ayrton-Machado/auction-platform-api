# auction-platform-api

![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

> API completa para sistema de leilões online com **autenticação JWT, criação de anúncios, sistema de lances, watchlist e comentários**. 
> Suporta **categorias, administração via Django Admin e controle de leilões ativos/fechados**.

### ✅ Concluído
- [x] API REST com Django REST Framework
- [x] Sistema de autenticação e registro
- [x] CRUD completo de leilões
- [x] Sistema de lances com validação
- [x] Watchlist e comentários
- [x] Testes unitários com pytest
- [x] Documentação com drf-spectacular

### 🚧 Em Desenvolvimento

**Funcionalidades Core:**
- [ ] Autenticação JWT (Substituir sessions)
- [ ] Sistema de notificações em tempo real (WebSockets)
- [ ] Paginação e filtros avançados
- [ ] Upload de múltiplas imagens

**Blockchain & Cripto:**
- [ ] Integração com Web3.py para Ethereum
- [ ] Suporte para Bitcoin via Lightning Network
- [ ] Smart contracts para escrow de leilões
- [ ] Carteira multi-signature
- [ ] Conversão automática de moedas (Oracle)

**IA de Confiança:**
- [ ] Criar repositório no Hugging Face Hub
- [ ] Modelo de análise de imagens (detectar produtos suspeitos)
- [ ] Modelo NLP para descrições (detectar fraudes)
- [ ] Sistema de score de confiabilidade
- [ ] Publicar modelo treinado no HF Hub
- [ ] Integrar API do Hugging Face

**DevOps & Infraestrutura:**
- [ ] Dockerização completa (Docker Compose)
- [ ] CI/CD com GitHub Actions
  - [ ] Testes automáticos em PRs
  - [ ] Lint e formatação (black, flake8, isort)
  - [ ] Build e push de imagens Docker
  - [ ] Deploy automático em staging
- [ ] Kubernetes para orquestração (opcional)
- [ ] Monitoramento com Prometheus + Grafana

**Deploy:**
- [ ] Backend no DigitalOcean Droplet (ou Railway/Render)
- [ ] PostgreSQL Managed Database
- [ ] Redis para cache e Celery
- [ ] DigitalOcean Spaces (S3-compatible) para imagens
- [ ] Frontend no Vercel/Netlify
- [ ] Domínio customizado + SSL (Let's Encrypt)
- [ ] CDN para assets estáticos

**Incrementar Cripto como Pagamento:**


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