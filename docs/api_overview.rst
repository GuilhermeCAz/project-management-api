Visão Geral da API
==================

A API de Gerenciamento de Projetos é uma API RESTful que permite gerenciar usuários, projetos e tarefas.

Base URL
--------

.. code-block::

   http://localhost:5000

Formato de Resposta
-------------------

Todas as respostas são retornadas em formato JSON.

Respostas de Sucesso
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "message": "Operação realizada com sucesso",
     "data": { ... }
   }

Respostas de Erro
~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Descrição do erro"
   }

Códigos de Status HTTP
----------------------

A API usa os seguintes códigos de status HTTP:

* ``200 OK`` - Requisição bem-sucedida
* ``201 Created`` - Recurso criado com sucesso
* ``400 Bad Request`` - Dados de entrada inválidos
* ``401 Unauthorized`` - Autenticação necessária
* ``403 Forbidden`` - Acesso negado
* ``404 Not Found`` - Recurso não encontrado
* ``409 Conflict`` - Conflito (ex: email já existe)
* ``500 Internal Server Error`` - Erro interno do servidor

Endpoints Principais
--------------------

Autenticação
~~~~~~~~~~~~

* ``POST /auth/login`` - Login do usuário
* ``POST /auth/register`` - Registro de novo usuário
* ``POST /auth/refresh`` - Renovar token de acesso
* ``POST /auth/logout`` - Logout do usuário
* ``GET /auth/verify`` - Verificar token

Usuários
~~~~~~~~

* ``GET /users`` - Listar usuários
* ``POST /users`` - Criar usuário (requer permissão de manager)
* ``GET /users/{id}`` - Obter usuário por ID
* ``PUT /users/{id}`` - Atualizar usuário (requer permissão de manager)
* ``DELETE /users/{id}`` - Deletar usuário (requer permissão de manager)

Projetos
~~~~~~~~

* ``GET /projects`` - Listar projetos
* ``POST /projects`` - Criar projeto (requer permissão de manager)
* ``GET /projects/{id}`` - Obter projeto por ID
* ``PUT /projects/{id}`` - Atualizar projeto (requer permissão de manager)
* ``DELETE /projects/{id}`` - Deletar projeto (requer permissão de manager)

Tarefas
~~~~~~~

* ``GET /projects/{project_id}/tasks`` - Listar tarefas de um projeto
* ``POST /projects/{project_id}/tasks`` - Criar tarefa (requer permissão de manager)
* ``GET /tasks/{id}`` - Obter tarefa por ID
* ``PUT /tasks/{id}`` - Atualizar tarefa (requer permissão de manager)
* ``DELETE /tasks/{id}`` - Deletar tarefa (requer permissão de manager)

Paginação
---------

Endpoints que retornam listas suportam paginação através dos parâmetros:

* ``limit`` - Número máximo de itens por página
* ``offset`` - Número de itens a pular

Exemplo:

.. code-block::

   GET /users?limit=10&offset=20

Filtros
-------

Muitos endpoints suportam filtros através de parâmetros de query:

* ``/users?user_type=manager`` - Filtrar usuários por tipo
* ``/projects?user_id=1`` - Filtrar projetos por proprietário
* ``/projects/{id}/tasks?status=pending`` - Filtrar tarefas por status