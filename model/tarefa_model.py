from database.database import MongoContext
from bson import ObjectId
import uuid


class TarefaModel:
    def __init__(self):
        """Inicializa o acesso à coleção de tarefas no banco de dados ou memória."""
        self.mongo_context = MongoContext()
        self.colecao = self.mongo_context.get_colecao()
        
        # Fallback para dados em memória quando não há conexão com MongoDB
        if not self.mongo_context.is_connected():
            self.tarefas_memoria = []
            print("Usando armazenamento em memória para as tarefas.")

    def listar(self, filtro_status=None):
        """Lista todas as tarefas, podendo filtrar por status."""
        if self.colecao is not None:
            # Usa MongoDB
            consulta = {}
            if filtro_status in ["Pendente", "Concluída"]:
                consulta = {"status": filtro_status}
            return list(self.colecao.find(consulta))
        else:
            # Usa memória
            if filtro_status in ["Pendente", "Concluída"]:
                return [t for t in self.tarefas_memoria if t["status"] == filtro_status]
            return self.tarefas_memoria.copy()

    def adicionar(self, titulo, descricao, status):
        """Adiciona uma nova tarefa ao banco de dados ou memória."""
        if self.colecao is not None:
            # Usa MongoDB
            return self.colecao.insert_one({"titulo": titulo, "descricao": descricao, "status": status})
        else:
            # Usa memória
            nova_tarefa = {
                "_id": str(uuid.uuid4()),
                "titulo": titulo,
                "descricao": descricao,
                "status": status
            }
            self.tarefas_memoria.append(nova_tarefa)
            return type('MockResult', (), {'inserted_id': nova_tarefa["_id"]})()

    def atualizar(self, id_tarefa, titulo, descricao, status):
        """Atualiza uma tarefa existente pelo id."""
        if self.colecao is not None:
            # Usa MongoDB
            return self.colecao.update_one({"_id": ObjectId(id_tarefa)}, {"$set": {"titulo": titulo, "descricao": descricao, "status": status}})
        else:
            # Usa memória
            for tarefa in self.tarefas_memoria:
                if tarefa["_id"] == id_tarefa:
                    tarefa["titulo"] = titulo
                    tarefa["descricao"] = descricao
                    tarefa["status"] = status
                    return type('MockResult', (), {'modified_count': 1})()
            return type('MockResult', (), {'modified_count': 0})()

    def excluir(self, id_tarefa):
        """Exclui uma tarefa do banco de dados ou memória pelo id."""
        if self.colecao is not None:
            # Usa MongoDB
            return self.colecao.delete_one({"_id": ObjectId(id_tarefa)})
        else:
            # Usa memória
            for i, tarefa in enumerate(self.tarefas_memoria):
                if tarefa["_id"] == id_tarefa:
                    del self.tarefas_memoria[i]
                    return type('MockResult', (), {'deleted_count': 1})()
            return type('MockResult', (), {'deleted_count': 0})()

    def buscar_por_id(self, id_tarefa):
        """Busca uma tarefa pelo id."""
        if self.colecao is not None:
            # Usa MongoDB
            return self.colecao.find_one({"_id": ObjectId(id_tarefa)})
        else:
            # Usa memória
            for tarefa in self.tarefas_memoria:
                if tarefa["_id"] == id_tarefa:
                    return tarefa
            return None
