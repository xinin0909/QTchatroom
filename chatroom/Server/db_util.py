from pymysql import *


class DBUtil(object):
    __doc__ = '''
    该类用来对数据库进行操作
    '''

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = 'root'
        self.database = 'chatroom'
        self.conn = None
        self.cur = None

    def connect_db(self):
        __doc__ = '''
        创建数据库连接对象
        :return: 数据库连接对象
        '''
        try:
            self.conn = connect(host=self.host, port=self.port, user=self.user,
                                password=self.password, database=self.database)
        except Exception as err:
            print("Error :", err)
            return None
        else:
            return self.conn

    def cur_db(self):
        __doc__ = '''
        创建游标对象
        :return:游标对象
        '''
        self.cur = self.conn.cursor()
        return self.cur

    def exc_sql(self, sql_stm, *args):
        __doc__ = '''
        执行SQL语句
        :param sql_stm:要执行的SQL语句
        :return: 执行是否成功
        '''
        try:
            result = self.cur.execute(sql_stm, args)
        except Exception as err:
            print("Error :", err)
            self.cur.close()
            self.conn.close()
            return False
        else:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return result

    def get_res(self, sql_stm, *args):
        __doc__ = '''
        执行查询语句
        :param sql_stm:要执行的SQL语句
        :return:返回查询到的结果 
        '''
        try:
            self.cur.execute(sql_stm, args)
        except Exception as err:
            print("Error :", err)
            self.cur.close()
            self.conn.close()
            return None
        else:
            data = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
            return data
