import customtkinter as ctk
from tkinter import ttk
from backend.Cliente_dao import Cliente_dao
from tkinter import messagebox

class GerenciarClientes(ctk.CTk):

    def __init__(self, db_conn):
        super().__init__()

        self.db_conn = db_conn 
        self.cliente_dao = Cliente_dao(self.db_conn) 
        self.tela_adicionar_cliente = None

        self.title("Gerenciamento de Clientes")
        self.geometry("920x600")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Clientes cadastrados", font=("Montserrat", 24))
        self.label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Endereço", "Telefone"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Telefone", text="Telefone")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("Endereço", width=200)
        self.tree.column("Telefone", width=150)

        self.inserir_dados()

        self.tree.pack(pady=20, fill="both", expand=True)

        self.button_add = ctk.CTkButton(
            self,
            text="Adicionar Cliente",
            command=self.abrir_tela_adicionar_cliente,
            fg_color="green", 
            hover_color="lightgreen" 
        )
        self.button_add.pack(pady=10, padx=(10, 5), side='left')

        self.button_remove = ctk.CTkButton(
            self,
            text="Remover Cliente",
            command=self.remover_cliente,
            fg_color="green",  
            hover_color="lightgreen"
        )
        self.button_remove.pack(pady=10, padx=(5, 5), side='left')

        self.button_update = ctk.CTkButton(
            self,
            text="Atualizar Cliente",
            command=self.atualizar_cliente,
            fg_color="green",  
            hover_color="lightgreen"  
        )
        self.button_update.pack(pady=10, padx=(5, 10), side='left')

        self.button_pets = ctk.CTkButton(
            self,
            text="Gerenciar Pets",
            command=self.gerenciar_pets,
            fg_color="gray",  
            hover_color="lightgray"
        )
        self.button_pets.pack(pady=10, padx=(10, 5), side='left')

        self.button_servicos = ctk.CTkButton(
            self,
            text="Gerenciar Serviços",
            command=self.gerenciar_servicos,
            fg_color="gray", 
            hover_color="lightgray" 
        )
        self.button_servicos.pack(pady=10, padx=(5, 5), side='left')

        self.button_sair = ctk.CTkButton(
            self,
            text="Sair",
            command=self.sair,
            fg_color="red",  
            hover_color="lightgray"
        )
        self.button_sair.pack(pady=10, padx=(5, 10), side='left')

    def abrir_tela(self, tela, cliente_dao=None):
        self.destroy() 
        nova_tela = tela(self.db_conn, cliente_dao) 
        nova_tela.mainloop() 

    def gerenciar_pets(self):
        from frontend.GerenciarPets import GerenciarPets 
        self.abrir_tela(GerenciarPets, self.cliente_dao)

    def gerenciar_servicos(self):
        from frontend.GerenciarServicos import GerenciarServicos 
        self.abrir_tela(GerenciarServicos, self.cliente_dao)  

    def sair(self):
        self.quit() 

    def inserir_dados(self):
        clientes = self.cliente_dao.listar_clientes()

        self.tree.delete(*self.tree.get_children())

        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)


    def abrir_tela_adicionar_cliente(self):
        if self.tela_adicionar_cliente is not None and self.tela_adicionar_cliente.winfo_exists():
            self.tela_adicionar_cliente.focus_force()
            return

        self.tela_adicionar_cliente = ctk.CTkToplevel(self)
        self.tela_adicionar_cliente.title("Adicionar Cliente")
        self.tela_adicionar_cliente.geometry("200x300")

        self.tela_adicionar_cliente.resizable(False, False)

        self.label_nome = ctk.CTkLabel(self.tela_adicionar_cliente, text="Nome:", font=("Montserrat", 14))
        self.label_nome.pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self.tela_adicionar_cliente)
        self.entry_nome.pack(pady=5)

        self.label_endereco = ctk.CTkLabel(self.tela_adicionar_cliente, text="Endereço:", font=("Montserrat", 14))
        self.label_endereco.pack(pady=5)
        self.entry_endereco = ctk.CTkEntry(self.tela_adicionar_cliente)
        self.entry_endereco.pack(pady=5)

        self.label_telefone = ctk.CTkLabel(self.tela_adicionar_cliente, text="Telefone:", font=("Montserrat", 14))
        self.label_telefone.pack(pady=5)
        self.entry_telefone = ctk.CTkEntry(self.tela_adicionar_cliente)
        self.entry_telefone.pack(pady=5)

        self.button_adicionar = ctk.CTkButton(self.tela_adicionar_cliente, text="Adicionar Cliente", command=self.adicionar_cliente)
        self.button_adicionar.pack(pady=10)

        self.tela_adicionar_cliente.protocol("WM_DELETE_WINDOW", self.on_close_adicionar_cliente)

    def on_close_adicionar_cliente(self):
        self.tela_adicionar_cliente.destroy() 
        self.tela_adicionar_cliente = None 

    def adicionar_cliente(self):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()

        if nome and endereco and telefone:
            self.cliente_dao.adicionar_cliente(nome, endereco, telefone)
            self.inserir_dados()
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.tela_adicionar_cliente.destroy()  
            self.tela_adicionar_cliente = None 
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

    def remover_cliente(self):
        selected_item = self.tree.selection() 
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum cliente selecionado para remoção.")
            return

        cliente_id = self.tree.item(selected_item)["values"][0]  

        if self.cliente_dao.remover_cliente(cliente_id):
            messagebox.showinfo("Sucesso", f"Cliente com ID {cliente_id} removido com sucesso.")
            self.tree.delete(selected_item) 
        else:
            messagebox.showerror("Erro", "Erro ao remover cliente.")

    def atualizar_cliente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum cliente selecionado para atualização.")
            return

        cliente_id = self.tree.item(selected_item)["values"][0]  
        cliente_nome = self.tree.item(selected_item)["values"][1]  
        cliente_endereco = self.tree.item(selected_item)["values"][2]  
        cliente_telefone = self.tree.item(selected_item)["values"][3]

        self.atualizar_cliente_window = ctk.CTkToplevel(self)
        self.atualizar_cliente_window.title("Atualizar Cliente")
        self.atualizar_cliente_window.geometry("200x200")
        self.atualizar_cliente_window.resizable(False, False)

        self.nome_entry = ctk.CTkEntry(self.atualizar_cliente_window, placeholder_text="Nome")
        self.nome_entry.pack(pady=10)
        self.nome_entry.insert(0, cliente_nome)

        self.endereco_entry = ctk.CTkEntry(self.atualizar_cliente_window, placeholder_text="Endereço")
        self.endereco_entry.pack(pady=10)
        self.endereco_entry.insert(0, cliente_endereco)

        self.telefone_entry = ctk.CTkEntry(self.atualizar_cliente_window, placeholder_text="Telefone")
        self.telefone_entry.pack(pady=10)
        self.telefone_entry.insert(0, cliente_telefone)

        self.button_update = ctk.CTkButton(self.atualizar_cliente_window, text="Atualizar Cliente",
                                            command=lambda: self.confirmar_atualizacao(cliente_id, cliente_nome, cliente_endereco, cliente_telefone))
        self.button_update.pack(pady=10)

    def confirmar_atualizacao(self, cliente_id, cliente_nome, cliente_endereco, cliente_telefone):
        novo_nome = self.nome_entry.get() or None 
        novo_endereco = self.endereco_entry.get() or None
        novo_telefone = self.telefone_entry.get() or None

        if self.cliente_dao.atualizar_cliente(cliente_id, novo_nome, novo_endereco, novo_telefone):
            messagebox.showinfo("Sucesso", f"Cliente com ID {cliente_id} atualizado com sucesso.")
            self.inserir_dados() 
            self.atualizar_cliente_window.destroy()
       
