# 🔗 Encurtador de URLs

Este projeto é um **encurtador de URLs** desenvolvido em **Python (Django)**.  
Ele permite encurtar links de forma rápida e segura e inclui funcionalidades para gerenciamento de usuários, envio de credenciais por e-mail e atualização de dados.

---

## 🚀 Instalação

1. Clone o repositório:

~~~bash
git clone <seu-repositorio>
cd <pasta-do-projeto>
~~~

2. Instale as dependências:

~~~bash
pip install -r requirements.txt
~~~

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo chamado **`.env`** na **raiz do projeto** (o mesmo diretório onde está `manage.py`).  
Não comite o `.env` no repositório — adicione-o ao `.gitignore`.

### Estrutura sugerida do `.env`

~~~env
# Configuração do Django
SECRET_KEY=chave_secreta_django
DEBUG=True #True para desenvolvimento, False para produção
ALLOWED_HOSTS= #Listar hosts separados por vírgula e sem espaço

# Configuração do usuário inicial (criado automaticamente ao rodar o servidor pela primeira vez)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@example.com

# Configuração de email (para envio de senha / notificações)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seuemail@gmail.com
EMAIL_HOST_PASSWORD=suasenha #usar senha de app do email

# Configurações do banco (exemplo)
DB_NAME=encurtador
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
~~~

**Observações importantes**
- O `.env` deve ficar na **raiz do projeto** (mesma pasta do `manage.py`).
- Se não existir nenhum usuário no banco, o sistema **cria automaticamente um usuário base** usando as variáveis `ADMIN_USERNAME`, `ADMIN_PASSWORD` e `ADMIN_EMAIL` do `.env`.
- Garanta que as credenciais de e-mail estejam corretas para que o envio de senha funcione.

---

## ⚡ Funcionalidades

- ✅ **Encurtamento de URLs** — cadastro e geração de links curtos.
- 👤 **Registro e autenticação de usuários** — criação de conta e login.
- 📩 **Envio de senha por e-mail** — ao registrar/recuperar, o sistema envia credenciais por e-mail.
- ✏️ **Alteração de dados de usuário** — usuário logado pode atualizar seu perfil (nome, senha, e-mail, etc).
- 🔒 Boas práticas: o `.env` mantém segredos fora do código, e senhas não devem ser logadas.

---

## ▶️ Executando o servidor (passo a passo)

> **Importante:** o banco de dados deve ser criado/inicializado usando o `Vagrantfile` fornecido no projeto antes de aplicar as migrações e iniciar o servidor.

1. Levante a máquina/ambiente via Vagrant (exemplo):

~~~bash
# na raiz do projeto (onde está o Vagrantfile)
vagrant up
vagrant ssh
~~~

2. Dentro da VM (ou conforme seu provisionamento), crie o banco de dados se necessário (exemplo usando psql):

~~~bash
# exemplo dentro da VM
psql -U postgres -c "CREATE DATABASE encurtador;"
# ou utilize o script de provisionamento que o Vagrantfile já fornece, se houver
~~~

3. Volte ao host (ou continue dentro do ambiente configurado) e aplique migrações:

~~~bash
python manage.py migrate
~~~

4. Inicie o servidor de desenvolvimento:
~~~bash
python manage.py runserver
~~~

