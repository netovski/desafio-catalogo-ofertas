# Desafio - Catálogo de Ofertas

Este repositório contém um sistema de catálogo de ofertas desenvolvido em Django, com um scraper integrado para coletar informações de produtos e exibi-los em uma interface web responsiva.

## Tecnologias Utilizadas
- Python 3.11.3
- Django
- Selenium
- PostgreSQL
- HTML, CSS (com Grid Layout para exibição responsiva)

## Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/desafio-catalogo-ofertas.git
cd desafio-catalogo-ofertas
```

### 2. Criar e Ativar um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados
Se estiver usando SQLite, o Django já estará configurado. Para PostgreSQL, configure `DATABASES` no `settings.py`.

Rodar as migrações:
```bash
python manage.py migrate
```

### 5. Criar um Superusuário
```bash
python manage.py createsuperuser
```

### 6. Executar o Scraper (opcional)
```bash
python manage.py shell
>>> from ofertas.scrapy import scrape_mercado_livre
>>> scrape_mercado_livre()
```

### 7. Iniciar o Servidor Django
```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/produtos` no navegador para visualizar a aplicação.

## Funcionalidades
- **Scraper Integrado:** Coleta informações de produtos automaticamente.
- **Filtro de Ofertas:** Permite filtrar por frete grátis e entrega Full.
- **Destaques:** Exibe o produto mais barato, mais caro, com maior desconto e com o link para redirecionamento direto.
- **Interface Responsiva:** Utiliza CSS Grid para exibição otimizada em diferentes telas.

## Licença
Este projeto é de uso livre, sem licença definida.



