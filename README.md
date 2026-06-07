# 🐦‍⬛Twitter Clone EBAC

Projeto final do curso **Desenvolvedor Full Stack Python** da EBAC.

A aplicação é um clone simplificado do Twitter, desenvolvido com **Python**, **Django**, **Django REST Framework** e **templates HTML/CSS**.

## Sobre o projeto

O objetivo deste projeto é criar uma rede social funcional baseada nos principais recursos de microblog, permitindo que usuários criem contas, editem seus perfis, sigam outros usuários, publiquem postagens, curtam e comentem conteúdos.

O projeto foi desenvolvido em arquitetura monolítica, com o front-end integrado ao Django por meio de templates, e também possui endpoints REST para as principais funcionalidades da aplicação.

## Funcionalidades

- Cadastro de usuários
- Login e logout
- Criação automática de perfil
- Edição de perfil
- Alteração de nome de exibição
- Alteração de biografia
- Upload de foto de perfil
- Alteração de e-mail
- Alteração de senha
- Sistema de seguir e deixar de seguir usuários
- Contagem de seguidores e seguindo
- Criação de postagens
- Edição de postagens próprias
- Exclusão de postagens próprias
- Feed com postagens apenas de usuários seguidos
- Curtidas em postagens
- Remoção de curtidas
- Comentários em postagens
- API REST com Django REST Framework
- Testes automatizados
- Integração contínua com GitHub Actions

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- HTML
- CSS
- Git
- GitHub Actions

## Estrutura principal do projeto

```txt
twitter-clone-ebac/
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── urls.py
│   └── tests.py
├── posts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── urls.py
│   └── tests.py
├── templates/
├── static/
├── media/
├── twitter_clone/
│   ├── settings.py
│   ├── urls.py
│   └── api_urls.py
├── manage.py
├── requirements.txt
└── README.md
```

## Models principais

O projeto utiliza os seguintes models principais:

- `Profile`: armazena informações extras do usuário, como nome de exibição, biografia e foto de perfil.
- `Follow`: controla o relacionamento de seguidores entre usuários.
- `Post`: representa uma postagem criada por um usuário.
- `Like`: representa uma curtida em uma postagem.
- `Comment`: representa um comentário em uma postagem.

## Endpoints principais da API

### Usuários

```txt
GET /api/users/
GET /api/users/<id>/
POST /api/users/<id>/follow/
GET /api/users/<id>/followers/
GET /api/users/<id>/following/
```

### Postagens

```txt
GET /api/posts/
POST /api/posts/
GET /api/posts/feed/
GET /api/posts/<id>/
PUT /api/posts/<id>/
PATCH /api/posts/<id>/
DELETE /api/posts/<id>/
POST /api/posts/<id>/like/
GET /api/posts/<id>/comments/
POST /api/posts/<id>/comments/
```

### Comentários

```txt
GET /api/comments/
POST /api/comments/
GET /api/comments/<id>/
PUT /api/comments/<id>/
PATCH /api/comments/<id>/
DELETE /api/comments/<id>/
```

## Como rodar o projeto localmente

Clone o repositório:

```bash
git clone https://github.com/ElMathidones/twitter-clone-ebac.git
```

Entre na pasta do projeto:

```bash
cd twitter-clone-ebac
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

No Windows:

```powershell
.\venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as migrations:

```bash
python manage.py migrate
```

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Rode o servidor:

```bash
python manage.py runserver
```

Acesse a aplicação:

```txt
http://127.0.0.1:8000/
```

Acesse o painel administrativo:

```txt
http://127.0.0.1:8000/admin/
```

## Como rodar os testes

Execute:

```bash
python manage.py test
```

O projeto possui testes para:

- criação automática de perfil;
- sistema de seguir e deixar de seguir usuários;
- cadastro de usuário;
- criação de postagens;
- edição de postagens;
- proteção contra edição de postagens de outros usuários;
- feed com postagens apenas de usuários seguidos;
- curtidas;
- comentários;
- endpoints da API REST.

## Autenticação da API

A API utiliza autenticação por sessão e autenticação básica do Django REST Framework.

Para testar pelo navegador, basta estar logado na aplicação e acessar:

```txt
http://127.0.0.1:8000/api/
```

## GitHub Actions

O projeto possui workflow de integração contínua com GitHub Actions.

A cada push ou pull request, o workflow executa:

- instalação das dependências;
- migrations;
- testes automatizados.

## Deploy

A aplicação está disponível em:

```txt
https://ElMathidones.pythonanywhere.com
```
O projeto foi publicado no PythonAnywhere com suporte a arquivos estáticos, arquivos de mídia, upload de foto de perfil e variáveis de ambiente.

## Autor

**Mathias Méndez**

GitHub: [ElMathidones](https://github.com/ElMathidones)
