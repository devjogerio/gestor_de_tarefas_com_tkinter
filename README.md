# Gerenciador de Tarefas (MVC)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Community-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

Este projeto é um gerenciador de tarefas com interface gráfica em Python, estruturado no padrão MVC (Model-View-Controller) e persistência de dados em MongoDB com sistema de fallback para armazenamento em memória.

## 🚀 Características

- **Arquitetura MVC** bem estruturada
- **Persistência MongoDB** com fallback automático para memória
- **Configuração via variáveis de ambiente**
- **Interface gráfica moderna** (CustomTkinter) com design responsivo
- **Cards visuais** para exibição de tarefas com ícones de status
- **Tema escuro/claro** automático baseado no sistema
- **Sistema robusto** com tratamento de erros
- **Testes automatizados** incluídos
- **Interface intuitiva** com seções organizadas e scroll

## 📋 Requisitos

- **Python 3.8+**
- **MongoDB Community Edition** (opcional - fallback automático)
- **Bibliotecas Python:**
  - customtkinter (interface gráfica moderna)
  - pymongo (conexão MongoDB)
  - python-dotenv (variáveis de ambiente)

## ⚙️ Instalação

### 1. Instalar Dependências Python
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Copie o arquivo de exemplo e configure:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=gerenciador_tarefas_db
COLLECTION_NAME=tarefas
```

### 3. Instalar MongoDB (Opcional)
**Windows:**
```bash
winget install MongoDB.Server
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

## 🏃‍♂️ Como Executar

### Executar Aplicação Principal
```bash
python main.py
```

### Executar Testes do Banco de Dados
```bash
python test_database.py
```

## ✨ Funcionalidades

### Operações CRUD Completas
- ✅ **Adicionar** novas tarefas com formulário intuitivo
- ✅ **Listar** todas as tarefas em cards visuais organizados
- ✅ **Atualizar** tarefas existentes com seleção por clique
- ✅ **Excluir** tarefas com confirmação visual
- ✅ **Filtrar** tarefas por status (Todos, Pendente, Concluída)

### Interface Moderna (CustomTkinter)
- 🎨 **Design moderno** com cantos arredondados e sombras
- 📱 **Layout responsivo** com scroll automático
- 🃏 **Cards visuais** para cada tarefa com ícones de status
- 🌓 **Tema automático** (escuro/claro) baseado no sistema
- ✨ **Animações suaves** e transições elegantes
- 📝 **Formulários organizados** em seções bem definidas
- 🎯 **Botões coloridos** com feedback visual ao hover

### Recursos Avançados
- 🔄 **Fallback automático** para memória quando MongoDB indisponível
- 🔧 **Configuração flexível** via variáveis de ambiente
- 🛡️ **Tratamento robusto de erros**
- 🧪 **Testes automatizados** para validação
- 💾 **Persistência confiável** com MongoDB

## 📁 Estrutura do Projeto

```
projeto-gerenciador-tarefas/
├── .env.example              # Exemplo de configuração
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação do projeto
├── requirements.txt         # Dependências Python
├── main.py                  # Ponto de entrada da aplicação
├── test_database.py         # Testes do banco de dados
├── controller/
│   └── tarefa_controller.py # Controlador MVC
├── database/
│   ├── contexto.py         # Contexto de conexão MongoDB
│   └── database.py         # Configuração do banco
├── model/
│   └── tarefa_model.py     # Modelo de dados das tarefas
└── view/
    └── tarefa_view.py      # Interface gráfica
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente Disponíveis

| Variável | Descrição | Valor Padrão |
|----------|-----------|-------------|
| `MONGO_URI` | URI de conexão MongoDB | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Nome do banco de dados | `gerenciador_tarefas_db` |
| `COLLECTION_NAME` | Nome da coleção | `tarefas` |

### Modo de Desenvolvimento

Para desenvolvimento, você pode usar o armazenamento em memória:
```bash
# Não configure MONGO_URI ou use uma URI inválida
# A aplicação automaticamente usará fallback em memória
python main.py
```

## 🧪 Testes

O projeto inclui um script de teste abrangente:

```bash
python test_database.py
```

**Testes incluídos:**
- ✅ Conexão com MongoDB
- ✅ Inserção de dados
- ✅ Listagem e filtros
- ✅ Busca por ID
- ✅ Atualização de registros
- ✅ Exclusão de dados

## 🚨 Solução de Problemas

### MongoDB não conecta
- Verifique se o serviço está rodando: `sc query MongoDB` (Windows)
- Confirme a URI no arquivo `.env`
- A aplicação funcionará em modo memória como fallback

### Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problemas de permissão
- Certifique-se de que o MongoDB tem permissões adequadas
- Execute como administrador se necessário (Windows)

## 🏗️ Arquitetura Técnica

### Padrão MVC Implementado

```mermaid
graph TD
    A[View - tarefa_view.py] --> B[Controller - tarefa_controller.py]
    B --> C[Model - tarefa_model.py]
    C --> D[Database - contexto.py]
    D --> E[(MongoDB)]
    D --> F[Memory Fallback]
    
    G[main.py] --> A
    H[.env] --> D
```

### Fluxo de Dados

1. **Interface Gráfica (View)**: Captura interações do usuário
2. **Controlador (Controller)**: Processa lógica de negócio
3. **Modelo (Model)**: Gerencia operações de dados
4. **Contexto de Banco**: Abstrai conexão MongoDB/Memória

### Componentes Principais

| Componente | Responsabilidade | Tecnologia |
|------------|------------------|------------|
| **View** | Interface gráfica moderna e interação | CustomTkinter |
| **Controller** | Lógica de negócio e coordenação | Python |
| **Model** | Operações CRUD e validação | PyMongo |
| **Database** | Conexão e contexto de dados | MongoDB/Memory |

## 📚 Exemplos de Uso

### Uso Básico da Interface Moderna

```bash
# Executar aplicação principal
python main.py
```

**Nova Interface CustomTkinter oferece:**

🎨 **Design Moderno:**
- Cards visuais para cada tarefa com ícones de status
- Tema escuro/claro automático baseado no sistema
- Cantos arredondados e sombras elegantes
- Botões coloridos com feedback visual

📱 **Funcionalidades Aprimoradas:**
1. ✏️ **Formulário organizado** em seções (Nova Tarefa, Ações, Filtros)
2. 🃏 **Cards de tarefas** com título, descrição truncada e ícone de status
3. 🔍 **Filtros visuais** por status (Todos, Pendente, Concluída)
4. 📝 **Seleção por clique** nos cards para edição
5. 🗑️ **Exclusão com confirmação** visual
6. 📜 **Scroll automático** para listas longas

**Ícones de Status:**
- ⏳ Tarefas Pendentes (laranja)
- ✅ Tarefas Concluídas (verde)

### Uso Programático do Model

```python
from model.tarefa_model import TarefaModel

# Inicializar modelo
model = TarefaModel()

# Adicionar tarefa
resultado = model.adicionar(
    titulo="Estudar Python",
    descricao="Revisar conceitos de POO",
    status="Pendente"
)

# Listar todas as tarefas
tarefas = model.listar()

# Filtrar por status
pendentes = model.listar("Pendente")
concluidas = model.listar("Concluída")

# Buscar por ID
tarefa = model.buscar_por_id(objeto_id)

# Atualizar tarefa
model.atualizar(
    id_tarefa,
    "Novo título",
    "Nova descrição",
    "Concluída"
)

# Excluir tarefa
model.excluir(id_tarefa)
```

### Configuração Personalizada

```python
# Arquivo .env personalizado
MONGO_URI=mongodb://usuario:senha@servidor:27017
DATABASE_NAME=meu_projeto_tarefas
COLLECTION_NAME=minhas_tarefas

# Para ambiente de desenvolvimento
MONGO_URI=  # Deixar vazio para usar memória
DATABASE_NAME=dev_tarefas
COLLECTION_NAME=tarefas_dev
```

## 📸 Interface Gráfica

### Tela Principal (CustomTkinter)
```
┌─────────────────────────────────────────────────────────┐
│                📋 Gerenciador de Tarefas                │
├─────────────────────────────────────────────────────────┤
│ ╭─────────────── ✏️ Nova Tarefa ───────────────╮       │
│ │ Título: [Digite o título da tarefa...]        │       │
│ │ Descrição: ┌─────────────────────────────────┐ │       │
│ │           │                                 │ │       │
│ │           └─────────────────────────────────┘ │       │
│ │ Status: [Pendente ▼]                          │       │
│ ╰───────────────────────────────────────────────╯       │
│                                                         │
│ ╭─────────────────── ⚡ Ações ──────────────────╮       │
│ │  [➕ Adicionar]  [✏️ Atualizar]  [🗑️ Excluir]  │       │
│ ╰─────────────────────────────────────────────────╯       │
│                                                         │
│ ╭─────────────────── 🔍 Filtros ─────────────────╮      │
│ │ Status: [Todos ▼]              [🔎 Filtrar]     │      │
│ ╰─────────────────────────────────────────────────╯      │
│                                                         │
│ ╭─────────────── 📝 Lista de Tarefas ──────────────╮    │
│ │ ╭─────────────────────────────────────────────╮   │    │
│ │ │ ⏳ Estudar Python                           │📝 │    │
│ │ │    Revisar conceitos de POO e...           │   │    │
│ │ ╰─────────────────────────────────────────────╯   │    │
│ │ ╭─────────────────────────────────────────────╮   │    │
│ │ │ ✅ Fazer exercícios                         │📝 │    │
│ │ │    Completar lista de exercícios...         │   │    │
│ │ ╰─────────────────────────────────────────────╯   │    │
│ ╰───────────────────────────────────────────────────╯    │
└─────────────────────────────────────────────────────────┘
```

## 📈 Melhorias Futuras

### ✅ Recentemente Implementado
- [x] **Interface moderna** com CustomTkinter
- [x] **Cards visuais** para exibição de tarefas
- [x] **Tema automático** escuro/claro
- [x] **Layout responsivo** com scroll
- [x] **Ícones de status** e feedback visual
- [x] **Seções organizadas** na interface

### Funcionalidades
- [ ] Implementar índices no MongoDB para otimização
- [ ] Adicionar validação de dados mais robusta
- [ ] Implementar paginação para grandes volumes
- [ ] Sistema de categorias e tags
- [ ] Notificações e lembretes
- [ ] Exportação para PDF/Excel
- [ ] Busca por texto nas tarefas
- [ ] Ordenação por data/prioridade

### Interface
- [ ] Modo de visualização em lista/grid
- [ ] Personalização de cores e temas
- [ ] Atalhos de teclado
- [ ] Drag & drop para reordenação
- [ ] Tooltips informativos
- [ ] Animações mais elaboradas

### Técnicas
- [ ] Adicionar logs estruturados
- [ ] Sistema de backup automático
- [ ] API REST para integração externa
- [ ] Testes unitários abrangentes
- [ ] CI/CD pipeline
- [ ] Containerização com Docker

### Interface
- [ ] Tema escuro/claro
- [ ] Atalhos de teclado
- [ ] Drag & drop para reordenação
- [ ] Calendário integrado
- [ ] Gráficos de produtividade

---

**Desenvolvido com ❤️ | 2025**

*Sistema robusto, seguro e escalável para gerenciamento de tarefas*
