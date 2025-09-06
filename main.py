from tkinter import Tk
from view.tarefa_view import TarefaView

"""Ponto de entrada da aplicação. Inicializa a interface gráfica principal."""

if __name__ == "__main__":
    root = Tk()
    app = TarefaView(root)
    root.mainloop()
