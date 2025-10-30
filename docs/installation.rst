Instalação
==========

Requisitos
----------

* Python 3.13+
* pip ou uv (recomendado)

Instalação do Projeto
---------------------

1. Clone o repositório:

.. code-block:: bash

   git clone <repository-url>
   cd project-management-api

2. Instale as dependências usando uv (recomendado):

.. code-block:: bash

   uv sync

Ou usando pip:

.. code-block:: bash

   pip install -e .

3. Configure as variáveis de ambiente:

.. code-block:: bash

   cp .env.example .env

Edite o arquivo `.env` com suas configurações:

.. code-block:: bash

   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///project_management.db
   FLASK_ENV=development

4. Execute a aplicação:

.. code-block:: bash

   python run.py

A API estará disponível em `http://localhost:5000`.

Configuração do Banco de Dados
------------------------------

A aplicação usa SQLAlchemy e por padrão cria um banco SQLite local. 
O banco de dados será criado automaticamente na primeira execução.

Para usar um banco de dados diferente, configure a variável `DATABASE_URL` no arquivo `.env`.
