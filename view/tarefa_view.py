import customtkinter as ctk
from controller.tarefa_controller import TarefaController
import tkinter as tk
import threading
import time

# Configuração do tema e aparência
ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ToolTip:
    """Classe para criar tooltips explicativos nos widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Exibe o tooltip quando o mouse entra no widget."""
        if self.tooltip_window or not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("Arial", "10", "normal"), padx=8, pady=4)
        label.pack(ipadx=1)
    
    def hide_tooltip(self, event=None):
        """Oculta o tooltip quando o mouse sai do widget."""
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

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
        self.modo_visualizacao = "lista"  # "lista" ou "grid"
        
        self._criar_widgets()
        self._configurar_atalhos_teclado()
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
        
        # Seção de configurações
        self._criar_secao_configuracoes()
        
        # Seção de lista de tarefas
        self._criar_secao_lista()
        
    def _configurar_atalhos_teclado(self):
        """Configura atalhos de teclado para ações frequentes."""
        # Ctrl+N - Nova tarefa (limpar campos)
        self.root.bind('<Control-n>', lambda e: self._limpar_campos_atalho())
        
        # Ctrl+S - Salvar/Adicionar tarefa
        self.root.bind('<Control-s>', lambda e: self._adicionar())
        
        # Ctrl+U - Atualizar tarefa selecionada
        self.root.bind('<Control-u>', lambda e: self._atualizar())
        
        # Delete - Excluir tarefa selecionada
        self.root.bind('<Delete>', lambda e: self._excluir())
        
        # Ctrl+F - Focar no filtro
        self.root.bind('<Control-f>', lambda e: self.combo_filtro.focus())
        
        # Enter no campo título - focar na descrição
        self.entrada_titulo.bind('<Return>', lambda e: self.texto_descricao.focus())
        
        # Ctrl+Enter - Adicionar tarefa de qualquer campo
        self.entrada_titulo.bind('<Control-Return>', lambda e: self._adicionar())
        self.texto_descricao.bind('<Control-Return>', lambda e: self._adicionar())
        
        # Ctrl+G - Alternar modo de visualização
        self.root.bind('<Control-g>', lambda e: self._alternar_modo_visualizacao())
        
    def _limpar_campos_atalho(self):
        """Limpa os campos e remove seleção (atalho Ctrl+N)."""
        self.limpar_campos()
        self.id_tarefa_selecionada = None
        self.entrada_titulo.focus()  # Foca no campo título
        
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
        ToolTip(self.entrada_titulo, "Digite um título descritivo para sua tarefa\nEnter: próximo campo | Ctrl+Enter: adicionar tarefa | Ctrl+N: limpar campos")
        
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
        ToolTip(self.texto_descricao, "Descreva detalhadamente o que precisa ser feito\nCtrl+Enter: adicionar tarefa")
        
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
        ToolTip(self.combo_status, "Selecione o status atual da tarefa")
        
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
        ToolTip(self.btn_adicionar, "Adiciona uma nova tarefa com os dados preenchidos nos campos acima\nAtalho: Ctrl+S")
        
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
        ToolTip(self.btn_atualizar, "Atualiza a tarefa selecionada com as informações dos campos\nAtalho: Ctrl+U")
        
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
        ToolTip(self.btn_excluir, "Remove permanentemente a tarefa selecionada da lista\nAtalho: Delete")
        
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
        ToolTip(self.combo_filtro, "Escolha qual tipo de tarefa deseja visualizar\nAtalho: Ctrl+F para focar")
        
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
        ToolTip(self.btn_filtrar, "Filtra a lista de tarefas pelo status selecionado")
        
    def _criar_secao_configuracoes(self):
        """Cria a seção de configurações de tema e cores."""
        config_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        config_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        config_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            config_frame, 
            text="🎨 Personalização", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=4, pady=(15, 10))
        
        # Modo de aparência
        ctk.CTkLabel(
            config_frame, 
            text="Tema:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.combo_tema = ctk.CTkComboBox(
            config_frame,
            values=["Light", "Dark", "System"],
            height=35,
            font=ctk.CTkFont(size=12),
            command=self._alterar_tema
        )
        self.combo_tema.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.combo_tema.set("Light")
        ToolTip(self.combo_tema, "Escolha entre tema claro, escuro ou automático do sistema")
        
        # Esquema de cores
        ctk.CTkLabel(
            config_frame, 
            text="Cores:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=2, padx=(20, 10), pady=5, sticky="w")
        
        self.combo_cores = ctk.CTkComboBox(
            config_frame,
            values=["blue", "green", "dark-blue", "red", "orange"],
            height=35,
            font=ctk.CTkFont(size=12),
            command=self._alterar_cores
        )
        self.combo_cores.grid(row=1, column=3, padx=(10, 20), pady=(5, 20), sticky="w")
        self.combo_cores.set("blue")
        ToolTip(self.combo_cores, "Selecione o esquema de cores da interface")
        
    def _alterar_tema(self, novo_tema):
        """Altera o tema da aplicação."""
        ctk.set_appearance_mode(novo_tema)
        
    def _alterar_cores(self, novo_esquema):
        """Altera o esquema de cores da aplicação."""
        ctk.set_default_color_theme(novo_esquema)
        # Reinicia a interface para aplicar as novas cores
        self._recriar_interface()
        
    def _recriar_interface(self):
        """Recria a interface para aplicar mudanças de cor."""
        # Limpa todos os widgets do frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Recria os widgets com as novas cores
        self._criar_secao_entrada()
        self._criar_secao_botoes()
        self._criar_secao_filtros()
        self._criar_secao_configuracoes()
        self._criar_secao_lista()
        
        # Recarrega as tarefas
        self.controller.carregar_tarefas()
        
    def _alternar_modo_visualizacao(self):
        """Alterna entre modo lista e grid com animação suave."""
        # Animação de fade-out
        self._animar_fade_out()
        
        # Aguarda um pouco para o fade-out
        self.root.after(150, self._completar_alternancia_modo)
        
    def _completar_alternancia_modo(self):
        """Completa a alternância de modo após o fade-out."""
        if self.modo_visualizacao == "lista":
            self.modo_visualizacao = "grid"
            self.btn_modo_visualizacao.configure(text="📋 Lista")
        else:
            self.modo_visualizacao = "lista"
            self.btn_modo_visualizacao.configure(text="🔲 Grid")
        
        # Reexibe as tarefas no novo modo com fade-in
        self.exibir_tarefas(self.tarefas_data)
        
    def _animar_fade_out(self):
        """Cria efeito de fade-out nos cards existentes."""
        for widget in self.tarefas_scroll_frame.winfo_children():
            # Simula fade-out alterando a opacidade visual
            try:
                widget.configure(fg_color=("gray85", "gray20"))
            except:
                pass  # Ignora widgets que não suportam fg_color
    
    def _animar_fade_in(self, widget):
        """Anima fade-in de um widget"""
        try:
            # Inicia com transparência simulada
            widget.configure(fg_color=("gray95", "gray15"))
            
            def fade_step(step):
                if step < 10:
                    # Gradualmente volta à cor normal
                    progress = step / 10.0
                    if progress < 0.5:
                        # Primeira metade: de cinza claro para cor normal
                        widget.configure(fg_color=("gray90", "gray18"))
                    else:
                        # Segunda metade: cor normal - remove o atributo para usar padrão
                        widget.configure(fg_color=("gray75", "gray25"))  # Cor padrão do CTkFrame
                    
                    self.root.after(30, lambda: fade_step(step + 1))
                else:
                    # Garante que termina com a cor padrão do CTkFrame
                    widget.configure(fg_color=("gray75", "gray25"))
            
            fade_step(0)
        except:
            # Se houver erro, apenas garante que o widget fica visível
            try:
                widget.configure(fg_color=("gray75", "gray25"))
            except:
                pass
        
    def _criar_secao_lista(self):
        """Cria a seção de lista de tarefas."""
        lista_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        lista_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Frame do cabeçalho da lista
        header_frame = ctk.CTkFrame(lista_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        ctk.CTkLabel(
            header_frame, 
            text="📝 Lista de Tarefas", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        # Botão para alternar visualização
        self.btn_modo_visualizacao = ctk.CTkButton(
            header_frame,
            text="🔲 Grid",
            command=self._alternar_modo_visualizacao,
            width=80,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        self.btn_modo_visualizacao.grid(row=0, column=1, sticky="e")
        ToolTip(self.btn_modo_visualizacao, "Alterna entre visualização em lista e grid\nAtalho: Ctrl+G")
        
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
        
        # Configura o grid baseado no modo de visualização
        if self.modo_visualizacao == "grid":
            # Modo grid: 2 colunas
            self.tarefas_scroll_frame.grid_columnconfigure(0, weight=1)
            self.tarefas_scroll_frame.grid_columnconfigure(1, weight=1)
            
            # Cria cards para cada tarefa em grid com animação
            for i, tarefa in enumerate(tarefas):
                row = i // 2
                col = i % 2
                self.root.after(i * 50, lambda t=tarefa, idx=i, r=row, c=col: self._criar_card_tarefa_grid_animado(t, idx, r, c))
        else:
            # Modo lista: 1 coluna
            self.tarefas_scroll_frame.grid_columnconfigure(0, weight=1)
            
            # Cria cards para cada tarefa em lista com animação
            for i, tarefa in enumerate(tarefas):
                self.root.after(i * 50, lambda t=tarefa, idx=i: self._criar_card_tarefa_animado(t, idx))
    
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
        ToolTip(select_btn, "Seleciona esta tarefa para edição ou exclusão")
        
    def _criar_card_tarefa_grid(self, tarefa, index, row, col):
        """Cria um card visual compacto para uma tarefa no modo grid."""
        # Frame do card (mais compacto para grid)
        card_frame = ctk.CTkFrame(self.tarefas_scroll_frame, corner_radius=10)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Ícone de status e título na mesma linha
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Ícone de status
        status_icon = "✅" if tarefa["status"] == "Concluída" else "⏳"
        status_color = "#2E8B57" if tarefa["status"] == "Concluída" else "#FF8C00"
        
        status_label = ctk.CTkLabel(
            header_frame,
            text=status_icon,
            font=ctk.CTkFont(size=16),
            text_color=status_color
        )
        status_label.grid(row=0, column=0, padx=(0, 8), sticky="w")
        
        # Título da tarefa (truncado para grid)
        titulo_truncado = tarefa["titulo"][:25] + "..." if len(tarefa["titulo"]) > 25 else tarefa["titulo"]
        titulo_label = ctk.CTkLabel(
            header_frame,
            text=titulo_truncado,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        titulo_label.grid(row=0, column=1, sticky="ew")
        
        # Descrição da tarefa (mais curta para grid)
        descricao_text = tarefa["descricao"][:50] + "..." if len(tarefa["descricao"]) > 50 else tarefa["descricao"]
        descricao_label = ctk.CTkLabel(
            card_frame,
            text=descricao_text,
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color="gray"
        )
        descricao_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
        
        # Botão de seleção (menor para grid)
        select_btn = ctk.CTkButton(
            card_frame,
            text="📝",
            width=60,
            height=25,
            command=lambda idx=index: self._selecionar_tarefa(idx),
            font=ctk.CTkFont(size=12)
        )
        select_btn.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        ToolTip(select_btn, "Seleciona esta tarefa para edição ou exclusão")
    
    def _criar_card_tarefa_grid_animado(self, tarefa, index, row, col):
        """Cria um card de tarefa no modo grid com animação de fade-in"""
        # Cria o card normalmente
        self._criar_card_tarefa_grid(tarefa, index, row, col)
        
        # Encontra o card recém-criado para aplicar animação
        try:
            # O card está na posição [row][col] do grid
            for widget in self.tarefas_scroll_frame.winfo_children():
                grid_info = widget.grid_info()
                if grid_info.get('row') == row and grid_info.get('column') == col:
                    # Aplica efeito de fade-in
                    self._animar_fade_in(widget)
                    break
        except:
            pass  # Se houver erro, o card aparece normalmente
    
    def _criar_card_tarefa_animado(self, tarefa, index):
        """Cria um card de tarefa no modo lista com animação de fade-in"""
        # Cria o card normalmente
        self._criar_card_tarefa(tarefa, index)
        
        # Encontra o card recém-criado para aplicar animação
        try:
            # O card está na posição [index] do grid
            for widget in self.tarefas_scroll_frame.winfo_children():
                grid_info = widget.grid_info()
                if grid_info.get('row') == index:
                    # Aplica efeito de fade-in
                    self._animar_fade_in(widget)
                    break
        except:
            pass  # Se houver erro, o card aparece normalmente
        
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
