import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class MongoContext:
    """Inicializa a conexão com o banco de dados MongoDB e define a coleção de tarefas."""
    def __init__(self):
        # Obtém configurações do ambiente ou usa valores padrão
        self.mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('MONGO_DATABASE', 'gerenciador_tarefas_db')
        self.collection_name = os.getenv('MONGO_COLLECTION', 'tarefas')
        
        try:
            # Inicializa a conexão com timeout reduzido para falhar mais rápido
            self.cliente = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Testa a conexão
            self.cliente.admin.command('ping')
            self.bd = self.cliente[self.database_name]
            self.colecao = self.bd[self.collection_name]
            self.connected = True
            print(f"Conectado ao MongoDB: {self.database_name}")
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            print(f"Erro ao conectar com MongoDB: {e}")
            print("A aplicação funcionará sem persistência de dados.")
            self.cliente = None
            self.bd = None
            self.colecao = None
            self.connected = False

    def get_colecao(self):
        """Retorna a coleção de tarefas do banco de dados."""
        return self.colecao if self.connected else None
    
    def is_connected(self):
        """Verifica se a conexão com o banco está ativa."""
        return self.connected
