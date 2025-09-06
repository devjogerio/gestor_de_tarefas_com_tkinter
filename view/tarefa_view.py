import tkinter as tk
from tkinter import ttk
from controller.tarefa_controller import TarefaController

class TarefaView:
    def __init__(self, root):
        """Inicializa a interface gráfica e conecta com o controller."""
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("950x700")
        self.root.configure(bg="#f0f0f0")
        self.controller = TarefaController(self)
        self.id_tarefa_selecionada = None
        self._criar_widgets()
        self.controller.carregar_tarefas()

    def _criar_widgets(self):
        """Cria e posiciona todos os widgets da interface gráfica."""
        quadro_entrada = tk.Frame(self.root, bg="#f0f0f0")
        quadro_entrada.pack(pady=10, padx=10, fill='x')
        tk.Label(quadro_entrada, text="Título da Tarefa:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entrada_titulo = tk.Entry(quadro_entrada, width=55, font=("Arial", 11))
        self.entrada_titulo.grid(row=0, column=1, columnspan=3, sticky='w', pady=5, padx=5)
        tk.Label(quadro_entrada, text="Descrição da Tarefa:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.texto_descricao = tk.Text(quadro_entrada, width=53, height=5, font=("Arial", 11))
        self.texto_descricao.grid(row=1, column=1, columnspan=3, sticky='w', pady=5, padx=5)
        tk.Label(quadro_entrada, text="Status:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.var_status = tk.StringVar()
        self.combo_status = ttk.Combobox(quadro_entrada, textvariable=self.var_status, values=["Pendente", "Concluída"], state='readonly', font=("Arial", 11))
        self.combo_status.grid(row=2, column=1, pady=5, padx=5)
        self.combo_status.current(0)
        quadro_botoes = tk.Frame(self.root, bg="#f0f0f0")
        quadro_botoes.pack(pady=10)
        tk.Button(quadro_botoes, text="Adicionar Tarefa", command=self._adicionar, bg="#a5d6a7", font=("Arial", 11, "bold"), width=18).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(quadro_botoes, text="Atualizar Tarefa", command=self._atualizar, bg="#fff59d", font=("Arial", 11, "bold"), width=18).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(quadro_botoes, text="Excluir Tarefa", command=self._excluir, bg="#ef9a9a", font=("Arial", 11, "bold"), width=18).grid(row=0, column=2, padx=10, pady=5)
        quadro_filtro = tk.Frame(self.root, bg="#f0f0f0")
        quadro_filtro.pack(pady=10)
        tk.Label(quadro_filtro, text="Filtrar por Status:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.var_filtro = tk.StringVar()
        self.combo_filtro = ttk.Combobox(quadro_filtro, textvariable=self.var_filtro, values=["Todos", "Pendente", "Concluída"], state='readonly', font=("Arial", 11))
        self.combo_filtro.current(0)
        self.combo_filtro.grid(row=0, column=1, padx=5)
        tk.Button(quadro_filtro, text="Aplicar Filtro", command=self._aplicar_filtro, bg="#81d4fa", font=("Arial", 11, "bold"), width=15).grid(row=0, column=2, padx=5)
        quadro_arvore = tk.Frame(self.root, bg="#f0f0f0")
        quadro_arvore.pack(pady=20, fill='both', expand=True)
        barra_rolagem = tk.Scrollbar(quadro_arvore, orient='vertical')
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)
        self.arvore_tarefas = ttk.Treeview(quadro_arvore, columns=("Título", "Descrição", "Status"), show="headings", height=15, yscrollcommand=barra_rolagem.set)
        self.arvore_tarefas.heading("Título", text="Título")
        self.arvore_tarefas.heading("Descrição", text="Descrição")
        self.arvore_tarefas.heading("Status", text="Status")
        self.arvore_tarefas.column("Título", width=220)
        self.arvore_tarefas.column("Descrição", width=480)
        self.arvore_tarefas.column("Status", width=120)
        self.arvore_tarefas.bind("<<TreeviewSelect>>", self._selecionar)
        self.arvore_tarefas.pack(pady=10, padx=10, fill='both', expand=True)
        barra_rolagem.config(command=self.arvore_tarefas.yview)

    def exibir_tarefas(self, tarefas):
        """Exibe a lista de tarefas no Treeview."""
        self.arvore_tarefas.delete(*self.arvore_tarefas.get_children())
        for tarefa in tarefas:
            self.arvore_tarefas.insert("", tk.END, values=(tarefa["titulo"], tarefa["descricao"], tarefa["status"]), iid=str(tarefa["_id"]))

    def limpar_campos(self):
        """Limpa os campos de entrada da interface."""
        self.entrada_titulo.delete(0, tk.END)
        self.texto_descricao.delete("1.0", tk.END)
        self.var_status.set("Pendente")

    def preencher_campos(self, tarefa):
        """Preenche os campos de entrada com os dados da tarefa selecionada."""
        self.entrada_titulo.delete(0, tk.END)
        self.entrada_titulo.insert(tk.END, tarefa["titulo"])
        self.texto_descricao.delete("1.0", tk.END)
        self.texto_descricao.insert(tk.END, tarefa["descricao"])
        self.var_status.set(tarefa["status"])

    def _adicionar(self):
        """Chama o controller para adicionar uma nova tarefa."""
        self.controller.adicionar_tarefa(self.entrada_titulo.get().strip(), self.texto_descricao.get("1.0", tk.END).strip(), self.var_status.get())

    def _atualizar(self):
        """Chama o controller para atualizar a tarefa selecionada."""
        self.controller.atualizar_tarefa(self.id_tarefa_selecionada, self.entrada_titulo.get().strip(), self.texto_descricao.get("1.0", tk.END).strip(), self.var_status.get())

    def _excluir(self):
        """Chama o controller para excluir a tarefa selecionada."""
        self.controller.excluir_tarefa(self.id_tarefa_selecionada)

    def _aplicar_filtro(self):
        """Aplica o filtro de status selecionado pelo usuário."""
        filtro = self.var_filtro.get()
        if filtro == "Todos":
            self.controller.carregar_tarefas()
        else:
            self.controller.carregar_tarefas(filtro)

    def _selecionar(self, event):
        """Obtém a tarefa selecionada no Treeview e solicita ao controller para preencher os campos."""
        selecionado = self.arvore_tarefas.selection()
        if selecionado:
            self.id_tarefa_selecionada = selecionado[0]
            self.controller.selecionar_tarefa(self.id_tarefa_selecionada)
