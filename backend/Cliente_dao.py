class Cliente_dao:

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def listar_clientes(self):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome_cliente, end_cliente, telefone FROM cliente")
            return cursor.fetchall()
        
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        
        finally:
            if 'cursor' in locals():
                cursor.close()

            if 'conn' in locals():
                conn.close()

    def adicionar_cliente(self, nome, endereco, telefone):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cliente (nome_cliente, end_cliente, telefone) VALUES (%s, %s, %s)",
                (nome, endereco, telefone)
            )
            conn.commit() 
            return True
        
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            return False  
        
        finally:
            if 'cursor' in locals():
                cursor.close()

            if 'conn' in locals():
                conn.close()

    def verificar_cliente_existe(self, id_dono):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cliente WHERE id = %s", (id_dono,))
            count = cursor.fetchone()[0]
            return count > 0  
        
        except Exception as e:
            print(f"Erro ao verificar cliente: {e}")
            return False
        
        finally:
            if 'cursor' in locals():
                cursor.close()

    def remover_cliente(self, cliente_id):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cliente WHERE id = %s", (cliente_id,))
            conn.commit()  
            return cursor.rowcount > 0 
        
        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
            return False
        
        finally:
            if 'cursor' in locals():
                cursor.close()

            if 'conn' in locals():
                conn.close()  

    def atualizar_cliente(self, cliente_id, novo_nome=None, novo_endereco=None, novo_telefone=None):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()

            set_clause = []
            params = []

            if novo_nome is not None:
                set_clause.append("nome_cliente = %s")
                params.append(novo_nome)

            if novo_endereco is not None:
                set_clause.append("end_cliente = %s")
                params.append(novo_endereco)

            if novo_telefone is not None:
                set_clause.append("telefone = %s")
                params.append(novo_telefone)

            if not set_clause:
                print("Nenhum campo para atualizar.")
                return False

            params.append(cliente_id) 

            sql = f"UPDATE cliente SET {', '.join(set_clause)} WHERE id = %s"
            cursor.execute(sql, params)
            conn.commit() 
            return cursor.rowcount > 0 
        
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False
        
        finally:
            if 'cursor' in locals():
                cursor.close()

            if 'conn' in locals():
                conn.close()

