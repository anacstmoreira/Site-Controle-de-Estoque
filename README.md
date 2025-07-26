# Sistema de Controle de Estoque com Flask

Este projeto é um sistema simples de controle de estoque desenvolvido com Python e Flask. Ele permite gerenciar itens com funcionalidades como cadastro, edição, exclusão e busca, com validações e mensagens de feedback ao usuário.

## Funcionalidades

- Cadastro de novos itens com os seguintes dados:
  - ID (único)
  - Nome
  - Marca
  - Descrição
  - Quantidade
  - Preço
- Listagem de itens com campo de busca
- Edição de itens existentes
- Exclusão de itens por ID
- Validações de entrada e tratamento de erros
- Uso de mensagens `flash` para retorno visual ao usuário

## Tecnologias utilizadas

- Python 3
- Flask
- HTML (Jinja2 para templates)
- SQLite (via módulo `database.py`)

## Como executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Instale as dependências:

   ```bash
   pip install flask
   ```

3. Inicie o servidor:

   ```bash
   python app.py
   ```

4. Acesse no navegador:

   ```
   http://localhost:5000
   ```

## Estrutura esperada do projeto

```
projeto/
├── app.py
├── database.py
├── templates/
│   ├── index.html
│   ├── novo.html
│   ├── editar.html
└── static/  (opcional, para CSS/JS)
```

## Observações

Este projeto foi desenvolvido com fins de aprendizado e prática em Flask para a faculdade.
