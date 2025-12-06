# Auction Platform API

![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

> **API REST para plataforma de leilões online** desenvolvida com **TDD**, seguindo **Clean Architecture** e aplicando princípios **SOLID**.
> 
> Arquitetura em camadas seguindo **SRP** com **95%+ de cobertura** em **85+ testes**, utilizando método **ZOMBIES**.

---

## 🔗 Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/register` | Registrar usuário |
| POST | `/api/auth/login` | Autenticar |
| POST | `/api/create_listing/` | Criar leilão |
| POST | `/api/listing/:id/bid` | Fazer lance |
| POST | `/api/listing/:id/close` | Fechar leilão (dono) |
| GET | `/api/auctions/` | Listar leilões ativos |
| GET | `/api/watchlist/` | Ver favoritos |

> 📖 **Documentação completa:** http://127.0.0.1:8000/api/docs

---

## 💻 Pré-requisitos

- [Python 3.13+](https://www.python.org/)
- pip (gerenciador de pacotes Python)
- Git

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Ayrton-Machado/auction-platform-api
cd auction-platform-api
```

### 2. Configure o ambiente virtual

#### Instale o virtualenv (se necessário)

```bash
pip install virtualenv
```

#### Crie e ative o ambiente virtual

**Linux/MacOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

> 💡 **Dica:** Você verá `(venv)` no início da linha de comando quando o ambiente estiver ativo.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário

```bash
python manage.py createsuperuser
```

## 💻 Usando

### Inicie o servidor

```bash
python manage.py runserver
```

### Executes os testes
```bash
pytest
```

### Verificar coverage
#### 1. Gerar .coverage
```bash
pytest --cov=auctions --cov-report=html --cov-report=term-missing
```

#### 2. Verificar retorno coverage
```bash
coverage report
```

✅ **Servidor disponível em:** http://127.0.0.1:8000/

---

## 🔐 Acessos Importantes

- **Admin:** http://127.0.0.1:8000/api/admin
- **Documentação:** http://127.0.0.1:8000/api/docs

---

## 📝 Desativar ambiente virtual

```bash
deactivate
```

---

## 📊 Progresso do Projeto

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
- [ ] Autenticação JWT (substituir sessions)
- [ ] Postgres (substituir SQLite3)
- [ ] Sistema de notificações em tempo real (WebSockets)
- [ ] Sistema de lances em tempo real (WebSockets)
- [ ] Paginação e filtros avançados
- [ ] Upload de múltiplas imagens

**Infraestrutura:**
- [ ] Dockerização completa (Docker Compose)
- [ ] CI/CD com GitHub Actions
  - [ ] Testes automáticos em PRs
- [ ] Monitoramento com Prometheus + Grafana

**Funcionalidades Futuras:**
- [ ] Implementação de IA + Dados
- [ ] Incrementar Cripto como Pagamento

---

## 📄 Licença

Este projeto está sob licença. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---