import customtkinter as ctk
from controller.tarefa_controller import TarefaController

# Configuração do tema e aparência
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TarefaView:
    def __init__(self, root):
        """Inicializa a interface gráfica moderna e conecta com o controller."""
        self.root = root
        self.root.title("🚀 Gerenciador de Tarefas Moderno")
        self.root.geometry("1200x800")
        
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.controller = TarefaController(self)
        self.id_tarefa_selecionada = None
        self.tarefas_data = []  # Armazenar dados das tarefas
        
        self._criar_widgets()
        self.controller.carregar_tarefas()

    def _criar_widgets(self):
        """Cria e posiciona todos os widgets da interface gráfica moderna."""
        # Título principal
        titulo_principal = ctk.CTkLabel(
            self.root, 
            text="📋 Gerenciador de Tarefas", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo_principal.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        
        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Seção de entrada de dados
        self._criar_secao_entrada()
        
        # Seção de botões de ação
        self._criar_secao_botoes()
        
        # Seção de filtros
        self._criar_secao_filtros()
        
        # Seção de lista de tarefas
        self._criar_secao_lista()
        
    def _criar_secao_entrada(self):
        """Cria a seção de entrada de dados."""
        # Frame de entrada
        entrada_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        entrada_frame.grid_columnconfigure(1, weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            entrada_frame, 
            text="✏️ Nova Tarefa", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=20)
        
        # Campo título
        ctk.CTkLabel(
            entrada_frame, 
            text="Título:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.entrada_titulo = ctk.CTkEntry(
            entrada_frame, 
            placeholder_text="Digite o título da tarefa...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entrada_titulo.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="ew")
        
        # Campo descrição
        ctk.CTkLabel(
            entrada_frame, 
            text="Descrição:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, padx=(20, 10), pady=5, sticky="nw")
        
        self.texto_descricao = ctk.CTkTextbox(
            entrada_frame, 
            height=100,
            font=ctk.CTkFont(size=14)
        )
        self.texto_descricao.grid(row=2, column=1, padx=(0, 20), pady=5, sticky="ew")
        
        # Campo status
        ctk.CTkLabel(
            entrada_frame, 
            text="Status:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=3, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.combo_status = ctk.CTkComboBox(
            entrada_frame,
            values=["Pendente", "Concluída"],
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.combo_status.grid(row=3, column=1, padx=(0, 20), pady=(5, 20), sticky="w")
        self.combo_status.set("Pendente")
        
    def _criar_secao_botoes(self):
        """Cria a seção de botões de ação."""
        botoes_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        botoes_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        botoes_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            botoes_frame, 
            text="⚡ Ações", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 10))
        
        # Botão adicionar
        self.btn_adicionar = ctk.CTkButton(
            botoes_frame,
            text="➕ Adicionar",
            command=self._adicionar,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        self.btn_adicionar.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ew")
        
        # Botão atualizar
        self.btn_atualizar = ctk.CTkButton(
            botoes_frame,
            text="✏️ Atualizar",
            command=self._atualizar,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF8C00",
            hover_color="#FF7F00"
        )
        self.btn_atualizar.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="ew")
        
        # Botão excluir
        self.btn_excluir = ctk.CTkButton(
            botoes_frame,
            text="🗑️ Excluir",
            command=self._excluir,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC143C",
            hover_color="#B22222"
        )
        self.btn_excluir.grid(row=1, column=2, padx=10, pady=(0, 20), sticky="ew")
        
    def _criar_secao_filtros(self):
        """Cria a seção de filtros."""
        filtros_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        filtros_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        filtros_frame.grid_columnconfigure(1, weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            filtros_frame, 
            text="🔍 Filtros", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 10))
        
        # Label filtro
        ctk.CTkLabel(
            filtros_frame, 
            text="Status:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0, padx=(20, 10), pady=5, sticky="w")
        
        # Combo filtro
        self.combo_filtro = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Pendente", "Concluída"],
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.combo_filtro.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.combo_filtro.set("Todos")
        
        # Botão aplicar filtro
        self.btn_filtrar = ctk.CTkButton(
            filtros_frame,
            text="🔎 Filtrar",
            command=self._aplicar_filtro,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4169E1",
            hover_color="#0000CD"
        )
        self.btn_filtrar.grid(row=1, column=2, padx=(10, 20), pady=(5, 20), sticky="e")
        
    def _criar_secao_lista(self):
        """Cria a seção de lista de tarefas."""
        lista_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        lista_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            lista_frame, 
            text="📝 Lista de Tarefas", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10))
        
        # Frame scrollável para as tarefas
        self.tarefas_scroll_frame = ctk.CTkScrollableFrame(
            lista_frame, 
            height=300,
            corner_radius=10
        )
        self.tarefas_scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.tarefas_scroll_frame.grid_columnconfigure(0, weight=1)

    def exibir_tarefas(self, tarefas):
        """Exibe as tarefas na interface gráfica moderna."""
        # Limpa tarefas existentes
        for widget in self.tarefas_scroll_frame.winfo_children():
            widget.destroy()
        
        # Armazena as tarefas para seleção
        self.tarefas_data = tarefas
        
        # Cria cards para cada tarefa
        for i, tarefa in enumerate(tarefas):
            self._criar_card_tarefa(tarefa, i)
    
    def _criar_card_tarefa(self, tarefa, index):
        """Cria um card visual para uma tarefa."""
        # Frame do card
        card_frame = ctk.CTkFrame(self.tarefas_scroll_frame, corner_radius=10)
        card_frame.grid(row=index, column=0, padx=10, pady=5, sticky="ew")
        card_frame.grid_columnconfigure(1, weight=1)
        
        # Ícone de status
        status_icon = "✅" if tarefa["status"] == "Concluída" else "⏳"
        status_color = "#2E8B57" if tarefa["status"] == "Concluída" else "#FF8C00"
        
        # Label do status
        status_label = ctk.CTkLabel(
            card_frame,
            text=status_icon,
            font=ctk.CTkFont(size=20),
            text_color=status_color
        )
        status_label.grid(row=0, column=0, rowspan=2, padx=(15, 10), pady=15, sticky="n")
        
        # Título da tarefa
        titulo_label = ctk.CTkLabel(
            card_frame,
            text=tarefa["titulo"],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        titulo_label.grid(row=0, column=1, padx=(0, 15), pady=(15, 5), sticky="ew")
        
        # Descrição da tarefa
        descricao_text = tarefa["descricao"][:100] + "..." if len(tarefa["descricao"]) > 100 else tarefa["descricao"]
        descricao_label = ctk.CTkLabel(
            card_frame,
            text=descricao_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            text_color="gray"
        )
        descricao_label.grid(row=1, column=1, padx=(0, 15), pady=(0, 15), sticky="ew")
        
        # Botão de seleção
        select_btn = ctk.CTkButton(
            card_frame,
            text="📝",
            width=40,
            height=30,
            command=lambda idx=index: self._selecionar_tarefa(idx),
            font=ctk.CTkFont(size=14)
        )
        select_btn.grid(row=0, column=2, rowspan=2, padx=(0, 15), pady=15)
        
    def _selecionar_tarefa(self, index):
        """Preenche os campos com os dados da tarefa selecionada."""
        if 0 <= index < len(self.tarefas_data):
            tarefa = self.tarefas_data[index]
            
            # Preenche título
            self.entrada_titulo.delete(0, "end")
            self.entrada_titulo.insert(0, tarefa["titulo"])
            
            # Preenche descrição
            self.texto_descricao.delete("1.0", "end")
            self.texto_descricao.insert("1.0", tarefa["descricao"])
            
            # Define status
            self.combo_status.set(tarefa["status"])
            
            # Armazena ID da tarefa selecionada
            self.id_tarefa_selecionada = str(tarefa["_id"])

    def limpar_campos(self):
        """Limpa os campos de entrada da interface."""
        self.entrada_titulo.delete(0, "end")
        self.texto_descricao.delete("1.0", "end")
        self.combo_status.set("Pendente")

    def preencher_campos(self, tarefa):
        """Preenche os campos de entrada com os dados da tarefa selecionada."""
        self.entrada_titulo.delete(0, "end")
        self.entrada_titulo.insert(0, tarefa["titulo"])
        self.texto_descricao.delete("1.0", "end")
        self.texto_descricao.insert("1.0", tarefa["descricao"])
        self.combo_status.set(tarefa["status"])

    def _adicionar(self):
        """Chama o controller para adicionar uma nova tarefa."""
        self.controller.adicionar_tarefa(self.entrada_titulo.get().strip(), self.texto_descricao.get("1.0", "end").strip(), self.combo_status.get())

    def _atualizar(self):
        """Chama o controller para atualizar a tarefa selecionada."""
        self.controller.atualizar_tarefa(self.id_tarefa_selecionada, self.entrada_titulo.get().strip(), self.texto_descricao.get("1.0", "end").strip(), self.combo_status.get())

    def _excluir(self):
        """Chama o controller para excluir a tarefa selecionada."""
        self.controller.excluir_tarefa(self.id_tarefa_selecionada)

    def _aplicar_filtro(self):
        """Aplica o filtro de status selecionado pelo usuário."""
        filtro = self.combo_filtro.get()
        if filtro == "Todos":
            self.controller.carregar_tarefas()
        else:
            self.controller.carregar_tarefas(filtro)

    def _selecionar(self, event):
        """Método mantido para compatibilidade (não usado na nova interface)."""
        pass
