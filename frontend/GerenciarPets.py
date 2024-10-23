import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from backend.Pet_dao import Pet_dao

class GerenciarPets(ctk.CTk):
    def __init__(self, db_conn, cliente_dao):
        super().__init__()

        self.db_conn = db_conn
        self.pet_dao = Pet_dao(self.db_conn)
        self.tela_adicionar_pet = None
        self.atualizar_pet_window = None
        self.cliente_dao = cliente_dao

        self.title("Gerenciamento de Pets")
        self.geometry("920x600")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Pets cadastrados", font=("Montserrat", 24))
        self.label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Raça", "Idade", "ID Dono"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Raça", text="Raça")
        self.tree.heading("Idade", text="Idade")
        self.tree.heading("ID Dono", text="ID Dono")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("Raça", width=150)
        self.tree.column("Idade", width=50)
        self.tree.column("ID Dono", width=100)

        self.inserir_dados()

        self.tree.pack(pady=20, fill="both", expand=True)

        self.button_add = ctk.CTkButton(
            self,
            text="Adicionar Pet",
            command=self.abrir_tela_adicionar_pet,
            fg_color="green", 
            hover_color="lightgreen"
        )
        self.button_add.pack(pady=10, padx=(10, 5), side='left')

        self.button_remove = ctk.CTkButton(
            self,
            text="Remover Pet",
            command=self.remover_pet,
            fg_color="green",
            hover_color="lightgreen"
        )    
        self.button_remove.pack(pady=10, padx=(5, 5), side='left')

        self.button_update = ctk.CTkButton(
            self,
            text="Atualizar Pet",
            command=self.atualizar_pet,
            fg_color="green",
            hover_color="lightgreen"
        )
        self.button_update.pack(pady=10, padx=(5, 10), side='left')

        self.button_clientes = ctk.CTkButton(
            self,
            text="Gerenciar Clientes",
            command=self.gerenciar_clientes,
            fg_color="gray",  
            hover_color="lightgray" 
        )
        self.button_clientes.pack(pady=10, padx=(10, 5), side='left')

        self.button_sair = ctk.CTkButton(
            self,
            text="Sair",
            command=self.sair,
            fg_color="red",  
            hover_color="lightgray" 
        )
        self.button_sair.pack(pady=10, padx=(5, 10), side='left')

    def abrir_tela(self, tela):
        self.destroy() 
        nova_tela = tela(self.db_conn) 
        nova_tela.mainloop() 

    def gerenciar_clientes(self):
        from frontend.GerenciarClientes import GerenciarClientes
        self.abrir_tela(GerenciarClientes)

    def sair(self):
        self.quit()

    def inserir_dados(self):
        pets = self.pet_dao.listar_pets()

        self.tree.delete(*self.tree.get_children())

        for pet in pets:
            self.tree.insert("", "end", values=(pet[0], pet[1], pet[2], pet[3], pet[4]))

    def abrir_tela_adicionar_pet(self):
        if self.tela_adicionar_pet is not None and self.tela_adicionar_pet.winfo_exists():
            self.tela_adicionar_pet.focus_force()
            return

        self.tela_adicionar_pet = ctk.CTkToplevel(self)
        self.tela_adicionar_pet.title("Adicionar Pet")
        self.tela_adicionar_pet.geometry("250x370")

        self.tela_adicionar_pet.resizable(False, False)

        self.label_nome = ctk.CTkLabel(self.tela_adicionar_pet, text="Nome:", font=("Montserrat", 14))
        self.label_nome.pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self.tela_adicionar_pet)
        self.entry_nome.pack(pady=5)

        self.label_raca = ctk.CTkLabel(self.tela_adicionar_pet, text="Raça:", font=("Montserrat", 14))
        self.label_raca.pack(pady=5)
        self.entry_raca = ctk.CTkEntry(self.tela_adicionar_pet)
        self.entry_raca.pack(pady=5)

        self.label_id_dono = ctk.CTkLabel(self.tela_adicionar_pet, text="ID do Dono:", font=("Montserrat", 14))
        self.label_id_dono.pack(pady=5)
        self.entry_id_dono = ctk.CTkEntry(self.tela_adicionar_pet)
        self.entry_id_dono.pack(pady=5)

        self.label_idade = ctk.CTkLabel(self.tela_adicionar_pet, text="Idade:", font=("Montserrat", 14))
        self.label_idade.pack(pady=5)
        self.entry_idade = ctk.CTkEntry(self.tela_adicionar_pet)
        self.entry_idade.pack(pady=5)

        self.button_adicionar = ctk.CTkButton(self.tela_adicionar_pet, text="Adicionar Pet", command=self.adicionar_pet)
        self.button_adicionar.pack(pady=10)

        self.tela_adicionar_pet.protocol("WM_DELETE_WINDOW", self.on_close_adicionar_pet)

    def on_close_adicionar_pet(self):
        self.tela_adicionar_pet.destroy()
        self.tela_adicionar_pet = None

    def adicionar_pet(self):
        nome = self.entry_nome.get()
        raca = self.entry_raca.get()
        id_dono = self.entry_id_dono.get()
        idade = self.entry_idade.get()

        if nome and raca and id_dono and idade:
            try:
                id_dono = int(id_dono)
            except ValueError:
                messagebox.showwarning("Atenção", "O ID do dono deve ser um número inteiro.")
                return

            if not self.cliente_dao.verificar_cliente_existe(id_dono):
                messagebox.showwarning("Atenção", "O ID do dono não existe.")
                return

            self.pet_dao.adicionar_pet(nome, raca, idade, id_dono)
            self.inserir_dados()
            messagebox.showinfo("Sucesso", "Pet adicionado com sucesso!")
            self.tela_adicionar_pet.destroy() 
            self.tela_adicionar_pet = None
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

    def remover_pet(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum pet selecionado para remoção.")
            return

        pet_id = self.tree.item(selected_item)["values"][0]

        if self.pet_dao.remover_pet(pet_id):
            messagebox.showinfo("Sucesso", f"Pet com ID {pet_id} removido com sucesso.")
            self.tree.delete(selected_item)
        else:
            messagebox.showerror("Erro", "Erro ao remover pet.")

    def atualizar_pet(self):
        if self.atualizar_pet_window is not None and self.atualizar_pet_window.winfo_exists():
            self.atualizar_pet_window.focus_force()
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum pet selecionado para atualização.")
            return

        pet_id = self.tree.item(selected_item)["values"][0] 
        pet_nome = self.tree.item(selected_item)["values"][1]  
        pet_raca = self.tree.item(selected_item)["values"][2] 
        pet_id_dono = self.tree.item(selected_item)["values"][4] 
        pet_idade = self.tree.item(selected_item)["values"][3]  

        self.atualizar_pet_window = ctk.CTkToplevel(self)
        self.atualizar_pet_window.title("Atualizar Pet")
        self.atualizar_pet_window.geometry("250x250")
        self.atualizar_pet_window.resizable(False, False)

        self.nome_entry = ctk.CTkEntry(self.atualizar_pet_window, placeholder_text="Nome")
        self.nome_entry.pack(pady=10)
        self.nome_entry.insert(0, pet_nome)

        self.raca_entry = ctk.CTkEntry(self.atualizar_pet_window, placeholder_text="Raça")
        self.raca_entry.pack(pady=10)
        self.raca_entry.insert(0, pet_raca)

        self.id_dono_entry = ctk.CTkEntry(self.atualizar_pet_window, placeholder_text="ID do Dono")
        self.id_dono_entry.pack(pady=10)
        self.id_dono_entry.insert(0, pet_id_dono)

        self.idade_entry = ctk.CTkEntry(self.atualizar_pet_window, placeholder_text="Idade")
        self.idade_entry.pack(pady=10)
        self.idade_entry.insert(0, pet_idade)

        self.button_update = ctk.CTkButton(self.atualizar_pet_window, text="Atualizar Pet",
                                            command=lambda: self.confirmar_atualizacao(pet_id))
        self.button_update.pack(pady=10)

    def confirmar_atualizacao(self, pet_id):
        novo_nome = self.nome_entry.get() or None
        novo_raca = self.raca_entry.get() or None
        novo_id_dono = self.id_dono_entry.get() or None
        novo_idade = self.idade_entry.get() or None

        if not self.cliente_dao.verificar_cliente_existe(novo_id_dono):
            messagebox.showwarning("Atenção", "O ID do dono não existe.")
            return 

        if novo_id_dono is not None:
            try:
                novo_id_dono = int(novo_id_dono)
            except ValueError:
                messagebox.showwarning("Atenção", "O ID do dono deve ser um número inteiro.")
                return

        if self.pet_dao.atualizar_pet(pet_id, novo_nome, novo_raca, novo_id_dono, novo_idade):
            messagebox.showinfo("Sucesso", f"Pet com ID {pet_id} atualizado com sucesso.")
            self.inserir_dados()
            self.atualizar_pet_window.destroy()
    
    def gerenciar_servicos(self):
        print("Abrindo tela de gerenciamento de serviços...")

    def sair(self):
        self.quit()
