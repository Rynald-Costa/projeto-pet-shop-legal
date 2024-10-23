import psycopg2
from psycopg2 import OperationalError

class Connect_db:
    def __init__(self, dbname="20221214010019", user="postgres", password="1234", host="localhost", port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Conexão estabelecida com sucesso!")
            
        except OperationalError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
        return self.conn

    def get_connection(self):
        if not self.conn or self.conn.closed:
            print("Nenhuma conexão ativa. Conectando ao banco de dados...")
            self.connect()
        return self.conn

    def login(self, username, password):
        try:
            db_cursor = self.conn.cursor()

            cmd_sql = "SELECT * FROM usuario WHERE username = %s AND senha = %s"
            db_cursor.execute(cmd_sql, (username, password))

            resultado = db_cursor.fetchone()
            return resultado is not None
        
        except psycopg2.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return False
        
        finally:
            if 'db_cursor' in locals():
                db_cursor.close()

