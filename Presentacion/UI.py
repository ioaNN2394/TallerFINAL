import tkinter as tk
from tkinter import messagebox, font
from TallerFINAL.LogicaNegocio.CRUD import CRUD

class BlogApp:

    def __init__(self, root):
        self.bd = CRUD.get_instance()
        self.root = root
        self.root.title("Blog App")

        title_font = font.Font(size=14, weight='bold')
        entry_font = font.Font(size=12)

        self.title_frame = tk.Frame(root)
        self.title_frame.pack(pady=10)
        self.title_label = tk.Label(self.title_frame, text="Título de la entrada:", font=title_font)
        self.title_label.pack(side='left')
        self.title_entry = tk.Entry(self.title_frame, font=entry_font)
        self.title_entry.pack(side='left')

        self.content_frame = tk.Frame(root)
        self.content_frame.pack(pady=10)
        self.content_label = tk.Label(self.content_frame, text="Contenido de la entrada:", font=title_font)
        self.content_label.pack(side='left')
        self.content_entry = tk.Entry(self.content_frame, font=entry_font)
        self.content_entry.pack(side='left')

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        self.create_button = tk.Button(self.button_frame, text="Crear entrada", command=self.create_entry, font=title_font)
        self.create_button.pack(side='left', padx=10)
        self.view_button = tk.Button(self.button_frame, text="Ver entradas", command=self.view_entries, font=title_font)
        self.view_button.pack(side='left', padx=10)

    def create_entry(self):
        title = self.title_entry.get()
        content = self.content_entry.get()
        self.bd.crear_entrada(title, content)
        messagebox.showinfo("Información", "Entrada creada con éxito")

    def view_entries(self):
        entries = self.bd.leer_entradas()
        for entry in entries:
            messagebox.showinfo("Entrada", f"ID: {entry['id']}\nTítulo: {entry['titulo']}\nContenido: {entry['contenido']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogApp(root)
    root.mainloop()