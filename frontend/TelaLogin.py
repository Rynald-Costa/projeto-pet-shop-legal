import customtkinter as ctk
import psycopg2 
from PIL import Image
from backend.Connect_db import Connect_db
from frontend.GerenciarClientes import GerenciarClientes

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Pet Shop Legal - Painel de Administrador")
        self.geometry("600x400")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1)  

        self.iconbitmap(r"C:\Users\Rynald\Documents\Visual Studio Code\Projeto Pet Shop\images\logo.ico")
        self.connect_db = Connect_db()

        self.cadastro_mode = False  
        self.create_widgets()

    def load_image(self):
        self.image = ctk.CTkImage(Image.open(r"Projeto Pet Shop/images/petshoplettering.png"), size=(300, 400))

        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.grid(row=0, column=0, rowspan=6, sticky="nsew") 

    def create_widgets(self):
        for widget in self.grid_slaves():
            widget.grid_forget()

        self.load_image()

        self.label_title = ctk.CTkLabel(self, text="Login" if not self.cadastro_mode else "Cadastrar Novo Usuário", font=("Montserrat", 24))
        self.label_title.grid(row=0, column=1, padx=20, pady=(10, 5))

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Usuário", font=("Montserrat", 14))
        self.entry_username.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*", font=("Montserrat", 14))
        self.entry_senha.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        if self.cadastro_mode:
            self.button_action = ctk.CTkButton(self, text="Cadastrar", font=("Montserrat", 14), command=self.cadastrar_usuario)
            self.button_action.grid(row=3, column=1, padx=20, pady=(10, 2), sticky="ew")
            self.button_voltar = ctk.CTkButton(self, text="Voltar", font=("Montserrat", 14), command=self.show_login)
            self.button_voltar.grid(row=4, column=1, padx=20, pady=(2, 10), sticky="ew")
        else:
            self.button_action = ctk.CTkButton(self, text="Entrar", font=("Montserrat", 14), command=self.login)
            self.button_action.grid(row=3, column=1, padx=20, pady=(10, 2), sticky="ew")
            self.button_cadastro = ctk.CTkButton(self, text="Cadastrar Novo Usuário", font=("Montserrat", 14), command=self.show_cadastro)
            self.button_cadastro.grid(row=4, column=1, padx=20, pady=(2, 10), sticky="ew")

        self.label_status = ctk.CTkLabel(self, text="", font=("Montserrat", 12))
        self.label_status.grid(row=5, column=1, padx=20, pady=5, sticky="n")

    def abrir_gerenciamento_clientes(self):
        root = GerenciarClientes(self.connect_db)
        root.mainloop()

    def login(self):
        username = self.entry_username.get()
        senha = self.entry_senha.get()

        if not username or not senha:
            self.label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")
            return

        if self.connect_db.login(username, senha):
            self.label_status.configure(text="Login realizado com sucesso!", text_color="green")
            
            self.destroy()  
            self.abrir_gerenciamento_clientes()
        else:
            self.label_status.configure(text="Usuário ou senha incorretos.", text_color="red")

    def show_cadastro(self):
        self.cadastro_mode = True
        self.create_widgets() 

    def show_login(self):
        self.cadastro_mode = False
        self.create_widgets()  

    def cadastrar_usuario(self):
        username = self.entry_username.get()
        senha = self.entry_senha.get()

        if not username or not senha:
            self.label_status.configure(text="Por favor, preencha todos os campos.", text_color="red")
            return

        try:
            conn = self.connect_db.get_connection() 
            cursor = conn.cursor()
           
            cursor.execute("INSERT INTO usuario (username, senha) VALUES (%s, %s)", (username, senha))
            conn.commit()
            self.label_status.configure(text="Usuário cadastrado com sucesso!", text_color="green")
            cursor.close()
            self.show_login()  

        except (Exception, psycopg2.DatabaseError) as error:
            self.label_status.configure(text="Erro ao cadastrar usuário: " + str(error), text_color="red")



