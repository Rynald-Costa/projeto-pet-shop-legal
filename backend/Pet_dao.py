class Pet_dao:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def listar_pets(self):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, nome_pet, raca_pet, idade, id_dono FROM pet")
            return cursor.fetchall()
        
        except Exception as e:
            print(f"Erro ao listar pets: {e}")
            return []
        
        finally:
            if 'cursor' in locals():
                cursor.close()

    def adicionar_pet(self, nome, raca, idade, id_dono):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pet (nome_pet, raca_pet, idade, id_dono) VALUES (%s, %s, %s, %s)",
                (nome, raca, idade, id_dono)
            )
            conn.commit()

        except Exception as e:
            print(f"Erro ao adicionar pet: {e}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def remover_pet(self, pet_id):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pet WHERE id = %s", (pet_id,))
            conn.commit() 
            return cursor.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao remover pet: {e}")
            return False
        
        finally:
            if 'cursor' in locals():
                cursor.close()

    def verificar_pet_existe(self, pet_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pet WHERE id_pet = %s", (pet_id,))
            count = cursor.fetchone()[0]
            return count > 0

    def atualizar_pet(self, pet_id, novo_nome=None, nova_raca=None, novo_id_dono=None, nova_idade=None):
        try:
            conn = self.db_conn.connect()
            cursor = conn.cursor()

            set_clause = []
            params = []

            if novo_nome is not None:
                set_clause.append("nome_pet = %s")
                params.append(novo_nome)

            if nova_raca is not None:
                set_clause.append("raca_pet = %s")
                params.append(nova_raca)

            if novo_id_dono is not None:
                set_clause.append("id_dono = %s")
                params.append(novo_id_dono)

            if nova_idade is not None:
                set_clause.append("idade = %s")
                params.append(nova_idade)

            if not set_clause:
                print("Nenhum campo para atualizar.")
                return False

            params.append(pet_id)

            sql = f"UPDATE pet SET {', '.join(set_clause)} WHERE id = %s"
            cursor.execute(sql, params)
            conn.commit() 
            return cursor.rowcount > 0 
        
        except Exception as e:
            print(f"Erro ao atualizar pet: {e}")
            return False
        
        finally:
            if 'cursor' in locals():
                cursor.close()
