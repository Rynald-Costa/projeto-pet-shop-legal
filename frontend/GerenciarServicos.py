import customtkinter as ctk
from tkinter import ttk, messagebox
from backend.Pet_dao import Pet_dao
from backend.Servicos_dao import Servicos_dao

class GerenciarServicos(ctk.CTk):

    def __init__(self, db_conn, cliente_dao=None):
        super().__init__()

        self.db_conn = db_conn
        self.servicos_dao = Servicos_dao(self.db_conn)
        self.cliente_dao = cliente_dao
        self.tela_adicionar = None
        self.tela_atualizar = None

        self.title("Gerenciamento de Serviços")
        self.geometry("920x600")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Serviços cadastrados", font=("Montserrat", 24))
        self.label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Descrição", "Valor", "ID Pet"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("ID Pet", text="ID Pet")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("Descrição", width=300)
        self.tree.column("Valor", width=100)
        self.tree.column("ID Pet", width=100)

        self.tree.pack(pady=20, fill="both", expand=True)

        self.inserir_dados()

        self.button_add = ctk.CTkButton(
            self,
            text="Adicionar Serviço",
            command=self.abrir_tela_adicionar_servico,
            fg_color="green",
            hover_color="lightgreen"
        )
        self.button_add.pack(pady=10, padx=(10, 5), side='left')

        self.button_remove = ctk.CTkButton(
            self,
            text="Remover Serviço",
            command=self.remover_servico,
            fg_color="green",
            hover_color="lightgreen"
        )
        self.button_remove.pack(pady=10, padx=(5, 5), side='left')

        self.button_update = ctk.CTkButton(
            self,
            text="Atualizar Serviço",
            command=self.abrir_tela_atualizar_servico,
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

    def inserir_dados(self):
        servicos = self.servicos_dao.listar_servicos()
        self.tree.delete(*self.tree.get_children())
        for servico in servicos:
            self.tree.insert("", "end", values=servico)

    def abrir_tela_adicionar_servico(self):
        if self.tela_adicionar is not None and self.tela_adicionar.winfo_exists():
            self.tela_adicionar.focus_force()
            return
        
        self.tela_adicionar = ctk.CTkToplevel(self)
        self.tela_adicionar.title("Adicionar Serviço")
        self.tela_adicionar.geometry("250x450")

        ctk.CTkLabel(self.tela_adicionar, text="Nome do Serviço").pack(pady=10)
        self.entry_nome = ctk.CTkEntry(self.tela_adicionar)
        self.entry_nome.pack(pady=5)

        ctk.CTkLabel(self.tela_adicionar, text="Descrição").pack(pady=10)
        self.entry_desc = ctk.CTkEntry(self.tela_adicionar)
        self.entry_desc.pack(pady=5)

        ctk.CTkLabel(self.tela_adicionar, text="Valor").pack(pady=10)
        self.entry_valor = ctk.CTkEntry(self.tela_adicionar)
        self.entry_valor.pack(pady=5)

        ctk.CTkLabel(self.tela_adicionar, text="ID do Pet").pack(pady=10)
        self.entry_id_pet = ctk.CTkEntry(self.tela_adicionar)
        self.entry_id_pet.pack(pady=5)

        ctk.CTkButton(self.tela_adicionar, text="Adicionar", command=self.adicionar_servico).pack(pady=20)

    def adicionar_servico(self):
        nome = self.entry_nome.get()
        descricao = self.entry_desc.get()
        valor = self.entry_valor.get()
        id_pet = self.entry_id_pet.get()

        if not all([nome, descricao, valor, id_pet]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            valor = float(valor) 
            self.servicos_dao.adicionar_servico(nome, descricao, valor, id_pet)
            messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso!")
            self.tela_adicionar.destroy()
            self.inserir_dados()
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar serviço: {e}")

    def abrir_tela_atualizar_servico(self):
        if self.tela_atualizar is not None and self.tela_atualizar.winfo_exists():
            self.tela_atualizar.focus_force()

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um serviço para atualizar.")
            return

        service_data = self.tree.item(selected_item)["values"]
        self.tela_atualizar = ctk.CTkToplevel(self)
        self.tela_atualizar.title("Atualizar Serviço")
        self.tela_atualizar.geometry("250x450")

        ctk.CTkLabel(self.tela_atualizar, text="Nome do Serviço").pack(pady=10)
        self.entry_nome_atualizar = ctk.CTkEntry(self.tela_atualizar)
        self.entry_nome_atualizar.insert(0, service_data[1])
        self.entry_nome_atualizar.pack(pady=5)

        ctk.CTkLabel(self.tela_atualizar, text="Descrição").pack(pady=10)
        self.entry_desc_atualizar = ctk.CTkEntry(self.tela_atualizar)
        self.entry_desc_atualizar.insert(0, service_data[2])
        self.entry_desc_atualizar.pack(pady=5)

        ctk.CTkLabel(self.tela_atualizar, text="Valor").pack(pady=10)
        self.entry_valor_atualizar = ctk.CTkEntry(self.tela_atualizar)
        self.entry_valor_atualizar.insert(0, service_data[3])
        self.entry_valor_atualizar.pack(pady=5)

        ctk.CTkLabel(self.tela_atualizar, text="ID do Pet").pack(pady=10)
        self.entry_id_pet_atualizar = ctk.CTkEntry(self.tela_atualizar)
        self.entry_id_pet_atualizar.insert(0, service_data[4])
        self.entry_id_pet_atualizar.pack(pady=5)

        ctk.CTkButton(self.tela_atualizar, text="Atualizar", command=lambda: self.atualizar_servico(service_data[0])).pack(pady=20)

    def atualizar_servico(self, servico_id):
            nome = self.entry_nome_atualizar.get()
            descricao = self.entry_desc_atualizar.get()
            valor = self.entry_valor_atualizar.get()
            id_pet = self.entry_id_pet_atualizar.get()

            if not all([nome, descricao, valor, id_pet]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return
            
            try:
                valor = float(valor)
                self.servicos_dao.atualizar_servico(servico_id, nome, descricao, valor, id_pet)
                messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
                self.tela_atualizar.destroy()
                self.inserir_dados()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar serviço: {e}")

    def remover_servico(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um serviço para remover.")
            return

        service_data = self.tree.item(selected_item)["values"]
        servico_id = service_data[0]

        try:
            self.servicos_dao.remover_servico(servico_id)
            messagebox.showinfo("Sucesso", "Serviço removido com sucesso!")
            self.inserir_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover serviço: {e}")

    def abrir_tela(self, tela, *args):
        self.destroy() 
        nova_tela = tela(*args)
        nova_tela.mainloop()

    def gerenciar_pets(self):
        from frontend.GerenciarPets import GerenciarPets
        self.abrir_tela(GerenciarPets, self.db_conn, self.cliente_dao, self.pet_dao)

    def gerenciar_clientes(self):
        from frontend.GerenciarClientes import GerenciarClientes
        self.abrir_tela(GerenciarClientes, self.db_conn)

    def sair(self):
        self.destroy()
