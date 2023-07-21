import sqlite3

class SqlData:

    def __init__(self, db):
        self.db = db
        # 连接数据库
        self.conn = sqlite3.connect(self.db)
        # 创建游标
        self.cursor = self.conn.cursor()

    # 创建表
    def create_table(self,table_name):
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ck TEXT NOT NULL UNIQUE,
            state INTEGER NOT NULL DEFAULT 0
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    # 插入数据
    def insertdata(self, table_name, ck,state):
        insert_data_sql = f'''
                INSERT INTO {table_name} (ck, state) VALUES (?, ?);
                '''
        self.cursor.execute(insert_data_sql, (ck, state))
        self.conn.commit()

    # 更新数据
    def updatedata(self, table_name, ck, new_state):
        update_data_sql = f'''
                UPDATE {table_name} SET state = ? WHERE ck = ?;
                '''
        self.cursor.execute(update_data_sql, (new_state, ck))
        self.conn.commit()

    # 读取数据
    def readdate(self, table_name):
        query_data_sql = f'''
                SELECT * FROM {table_name};
                '''
        self.cursor.execute(query_data_sql)
        return self.cursor.fetchall()


    def closedb(self):
        self.cursor.close()
        self.conn.close()

