# Gerenciador de Tarefas (MVC)

Este projeto é um gerenciador de tarefas com interface gráfica em Python, estruturado no padrão MVC (Model-View-Controller) e persistência de dados em MongoDB com sistema de fallback para armazenamento em memória.

## 🚀 Características

- **Arquitetura MVC** bem estruturada
- **Persistência MongoDB** com fallback automático para memória
- **Configuração via variáveis de ambiente**
- **Interface gráfica intuitiva** (Tkinter)
- **Sistema robusto** com tratamento de erros
- **Testes automatizados** incluídos

## 📋 Requisitos

- **Python 3.8+**
- **MongoDB Community Edition** (opcional - fallback automático)
- **Bibliotecas Python:**
  - tkinter (incluso no Python)
  - pymongo
  - python-dotenv

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
- ✅ **Adicionar** novas tarefas
- ✅ **Listar** todas as tarefas ou filtrar por status
- ✅ **Atualizar** tarefas existentes
- ✅ **Excluir** tarefas
- ✅ **Buscar** tarefas por ID

### Recursos Avançados
- 🔄 **Fallback automático** para memória quando MongoDB indisponível
- 🔧 **Configuração flexível** via variáveis de ambiente
- 🛡️ **Tratamento robusto de erros**
- 🎨 **Interface gráfica intuitiva** com Tkinter
- 🧪 **Testes automatizados** para validação

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

## 📈 Melhorias Futuras

- [ ] Implementar índices no MongoDB para otimização
- [ ] Adicionar validação de dados mais robusta
- [ ] Implementar paginação para grandes volumes
- [ ] Adicionar logs estruturados
- [ ] Sistema de backup automático
- [ ] API REST para integração externa

---

**Desenvolvido com ❤️ | 2025**

*Sistema robusto, seguro e escalável para gerenciamento de tarefas*
