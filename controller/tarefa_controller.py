from model.tarefa_model import TarefaModel
from tkinter import messagebox

class TarefaController:
    def __init__(self, view):
        """Inicializa o controller com a view e o model."""
        self.model = TarefaModel()
        self.view = view
        self.id_tarefa_selecionada = None

    def carregar_tarefas(self, filtro_status=None):
        """Carrega as tarefas do model e envia para a view exibir."""
        tarefas = self.model.listar(filtro_status)
        self.view.exibir_tarefas(tarefas)

    def adicionar_tarefa(self, titulo, descricao, status):
        """Adiciona uma nova tarefa usando o model e atualiza a view."""
        if not titulo:
            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")
            return
        self.model.adicionar(titulo, descricao, status)
        self.carregar_tarefas()
        self.view.limpar_campos()
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

    def atualizar_tarefa(self, id_tarefa, titulo, descricao, status):
        """Atualiza uma tarefa existente pelo id usando o model e atualiza a view."""
        if not id_tarefa:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada para atualizar.")
            return
        if not titulo:
            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")
            return
        self.model.atualizar(id_tarefa, titulo, descricao, status)
        self.carregar_tarefas()
        self.view.limpar_campos()
        self.id_tarefa_selecionada = None
        messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")

    def excluir_tarefa(self, id_tarefa):
        """Exclui uma tarefa pelo id usando o model e atualiza a view."""
        if not id_tarefa:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir esta tarefa?")
        if confirmar:
            self.model.excluir(id_tarefa)
            self.carregar_tarefas()
            self.view.limpar_campos()
            self.id_tarefa_selecionada = None
            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")

    def aplicar_filtro(self, filtro_status):
        """Aplica filtro de status nas tarefas."""
        self.carregar_tarefas(filtro_status)

    def selecionar_tarefa(self, id_tarefa):
        """Seleciona uma tarefa pelo id e preenche os campos na view."""
        tarefa = self.model.buscar_por_id(id_tarefa)
        if tarefa:
            self.id_tarefa_selecionada = id_tarefa
            self.view.preencher_campos(tarefa)
