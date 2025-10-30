Autenticação
============

A API usa autenticação baseada em JWT (JSON Web Tokens) para proteger os endpoints.

Tipos de Token
--------------

Access Token
~~~~~~~~~~~~

* Usado para autenticar requisições à API
* Tempo de vida curto (recomendado: 15-30 minutos)
* Deve ser incluído no header ``Authorization`` como ``Bearer <token>``

Refresh Token
~~~~~~~~~~~~~

* Usado para obter novos access tokens
* Tempo de vida longo (recomendado: 7-30 dias)
* Armazenado de forma segura no cliente

Fluxo de Autenticação
---------------------

1. **Login**: O usuário faz login com email e senha
2. **Tokens**: A API retorna access token e refresh token
3. **Requisições**: O cliente inclui o access token nas requisições
4. **Renovação**: Quando o access token expira, use o refresh token para obter um novo
5. **Logout**: Invalide os tokens no logout

Exemplos de Uso
---------------

Login
~~~~~

.. code-block:: http

   POST /auth/login
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "password123"
   }

Resposta:

.. code-block:: json

   {
     "message": "Login successful",
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "user": {
       "id": 1,
       "name": "John Doe",
       "email": "user@example.com",
       "user_type": "employee"
     }
   }

Usando o Access Token
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   GET /users
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Renovando o Token
~~~~~~~~~~~~~~~~~

.. code-block:: http

   POST /auth/refresh
   Content-Type: application/json

   {
     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }

Resposta:

.. code-block:: json

   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }

Logout
~~~~~~

.. code-block:: http

   POST /auth/logout
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Verificação de Token
~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   GET /auth/verify
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Tipos de Usuário
----------------

A API suporta dois tipos de usuário:

Manager
~~~~~~~

* Pode criar, atualizar e deletar usuários
* Pode criar, atualizar e deletar projetos
* Pode criar, atualizar e deletar tarefas
* Acesso total à API

Employee
~~~~~~~~

* Pode visualizar usuários, projetos e tarefas
* Não pode criar, atualizar ou deletar recursos
* Acesso limitado à API

Tratamento de Erros
-------------------

Erros de Autenticação
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Invalid email or password"
   }

Token Inválido
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Invalid or expired token"
   }

Acesso Negado
~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Access denied. Manager role required"
   }