# Gerenciador de Tarefas (MVC)

Este projeto é um gerenciador de tarefas com interface gráfica em Python, estruturado no padrão MVC (Model-View-Controller) e persistência de dados em MongoDB.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação.
- `model/`: Contém o modelo de dados e acesso ao banco.
- `view/`: Interface gráfica (Tkinter).
- `controller/`: Lógica de controle entre view e model.
- `contexto/`: Contexto de conexão com o MongoDB.

## Requisitos

- Python 3.8+
- MongoDB em execução local
- Bibliotecas:
  - tkinter (incluso no Python)
  - pymongo
  - bson

## Instalação

1. Instale as dependências:
   ```bash
   pip install pymongo bson
   ```
2. Certifique-se de que o MongoDB está rodando em `localhost:27017`.

## Como executar

1. Execute o arquivo principal:
   ```bash
   python main.py
   ```

## Funcionalidades

- Adicionar, atualizar e excluir tarefas
- Filtrar tarefas por status
- Interface gráfica amigável
- Persistência de dados em MongoDB

## Estrutura de Pastas

```
projeto-gerenciador-tarefas/
├── main.py
├── model/
│   └── tarefa_model.py
├── view/
│   └── tarefa_view.py
├── controller/
│   └── tarefa_controller.py
├── contexto/
│   └── contexto.py
└── README.md
```

---

Desenvolvido por devjogerio | 2025
