from pymongo import MongoClient

class MongoContext:
    """Inicializa a conexão com o banco de dados MongoDB e define a coleção de tarefas."""
    def __init__(self):
        self.cliente = MongoClient("mongodb://localhost:27017/")
        self.bd = self.cliente["gerenciador_tarefas_db"]
        self.colecao = self.bd["tarefas"]

    def get_colecao(self):
        """Retorna a coleção de tarefas do banco de dados."""
        return self.colecao
