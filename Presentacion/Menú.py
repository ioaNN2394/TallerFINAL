from LogicaNegocio.CRUD import CRUD

from tkinter import *
from tkinter import messagebox, simpledialog

class Menu:
    def __init__(self, bd, root):
        self.bd = bd
        self.root = root
        self.root.title("Blog")
        self.root.geometry("400x300")  # Tamaño personalizado
        self.menu()

    def menu(self):
        Label(self.root, text="Elige una opción:", font=("Helvetica", 14)).pack(pady=10)  # Fuente y espacio alrededor
        options_frame = Frame(self.root)  # Frame para los botones
        options_frame.pack(pady=5)

        # Botones con estilo simétrico
        Button(options_frame, text="Crear entrada", width=15, command=self.opcion_crear_entrada).grid(row=0, column=0, padx=5)
        Button(options_frame, text="Ver entradas", width=15, command=self.opcion_ver_entradas).grid(row=0, column=1, padx=5)
        Button(options_frame, text="Ver entrada específica", width=15, command=self.opcion_ver_entrada_especifica).grid(row=1, column=0, padx=5)
        Button(options_frame, text="Actualizar entrada", width=15, command=self.opcion_actualizar_entrada).grid(row=1, column=1, padx=5)
        Button(options_frame, text="Eliminar entrada", width=15, command=self.opcion_eliminar_entrada).grid(row=2, column=0, columnspan=2, pady=5)

        # Botón de salir alineado a la derecha
        Button(self.root, text="Salir", width=10, command=self.opcion_salir).pack(side=RIGHT, padx=10, pady=5)

    def opcion_crear_entrada(self):
        titulo = simpledialog.askstring("Input", "Introduce el título de la entrada: ")
        contenido = simpledialog.askstring("Input", "Introduce el contenido de la entrada: ")
        self.bd.crear_entrada(titulo, contenido)
        messagebox.showinfo("Mensaje", "Entrada creada exitosamente.")

    def opcion_ver_entradas(self):
        entradas = self.bd.leer_entradas()
        messagebox.showinfo("Entradas", "\n\n".join(
            [f"Título: {entrada['titulo']}\nContenido: {entrada['contenido']}" for entrada in entradas]))

    def opcion_ver_entrada_especifica(self):
        id_entrada = simpledialog.askstring("Input", "Introduce el ID de la entrada a leer: ")
        entrada = self.bd.leer_entrada(id_entrada)
        if entrada:
            messagebox.showinfo("Entrada", f"Título: {entrada['titulo']}\nContenido: {entrada['contenido']}")
        else:
            messagebox.showinfo("Mensaje", "No se encontró la entrada con el ID especificado.")


    def opcion_actualizar_entrada(self):
        id_entrada = simpledialog.askstring("Input", "Introduce el ID de la entrada a actualizar: ")
        titulo = simpledialog.askstring("Input", "Introduce el nuevo título de la entrada: ")
        contenido = simpledialog.askstring("Input", "Introduce el nuevo contenido de la entrada: ")
        message = self.bd.actualizar_entrada(id_entrada, titulo, contenido)
        messagebox.showinfo("Mensaje", message)

    def opcion_eliminar_entrada(self):
        id_entrada = simpledialog.askstring("Input", "Introduce el ID de la entrada a eliminar: ")
        message = self.bd.eliminar_entrada(id_entrada)
        messagebox.showinfo("Mensaje", message)
    def opcion_salir(self):
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    bd = CRUD.get_instance()  # Create an instance of CRUD
    menu = Menu(bd, root)  # Pass the instance of CRUD as the first argument
    menu.run()
