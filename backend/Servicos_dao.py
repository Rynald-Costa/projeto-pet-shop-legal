class Servicos_dao:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def listar_servicos(self):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome_serv, desc_serv, valor_serv, id_pet FROM servicos")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar serviços: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

    def adicionar_servico(self, nome_serv, desc_serv, valor_serv, id_pet):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO servicos (nome_serv, desc_serv, valor_serv, id_pet) VALUES (%s, %s, %s, %s)",
                (nome_serv, desc_serv, valor_serv, id_pet)
            )
            conn.commit()
        except Exception as e:
            print(f"Erro ao adicionar serviço: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def remover_servico(self, servico_id):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM servicos WHERE id = %s", (servico_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao remover serviço: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def atualizar_servico(self, servico_id, novo_nome=None, nova_desc=None, novo_valor=None, novo_id_pet=None):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()

            set_clause = []
            params = []

            if novo_nome:
                set_clause.append("nome_serv = %s")
                params.append(novo_nome)
            if nova_desc:
                set_clause.append("desc_serv = %s")
                params.append(nova_desc)
            if novo_valor:
                set_clause.append("valor_serv = %s")
                params.append(novo_valor)
            if novo_id_pet:
                set_clause.append("id_pet = %s")
                params.append(novo_id_pet)

            if not set_clause:
                print("Nenhum campo para atualizar.")
                return False

            params.append(servico_id)

            sql = f"UPDATE servicos SET {', '.join(set_clause)} WHERE id = %s"
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar serviço: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
