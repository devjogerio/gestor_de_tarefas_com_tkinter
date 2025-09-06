from bson.objectid import ObjectId
from database.database import MongoContext

class TarefaModel:
    def __init__(self):
        """Inicializa o acesso à coleção de tarefas no banco de dados."""
        self.colecao = MongoContext().get_colecao()

    def listar(self, filtro_status=None):
        """Lista todas as tarefas, podendo filtrar por status."""
        consulta = {}
        if filtro_status in ["Pendente", "Concluída"]:
            consulta = {"status": filtro_status}
        return list(self.colecao.find(consulta))

    def adicionar(self, titulo, descricao, status):
        """Adiciona uma nova tarefa ao banco de dados."""
        return self.colecao.insert_one({"titulo": titulo, "descricao": descricao, "status": status})

    def atualizar(self, id_tarefa, titulo, descricao, status):
        """Atualiza uma tarefa existente pelo id."""
        return self.colecao.update_one({"_id": ObjectId(id_tarefa)}, {"$set": {"titulo": titulo, "descricao": descricao, "status": status}})

    def excluir(self, id_tarefa):
        """Exclui uma tarefa do banco de dados pelo id."""
        return self.colecao.delete_one({"_id": ObjectId(id_tarefa)})

    def buscar_por_id(self, id_tarefa):
        """Busca uma tarefa pelo id."""
        return self.colecao.find_one({"_id": ObjectId(id_tarefa)})
