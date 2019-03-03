from db_util import DBUtil
from user_info import User


class Group(object):
    def __init__(self, admin_id, group_name):
        self.admin_id = admin_id
        self.group_name = group_name

    def create_group(self):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "insert into group_info(group_admin_id,group_name) values({},'{}')"\
            .format(self.admin_id, self.group_name)
        result1 = db.exc_sql(sql_stm)
        if result1:
            result2 = self.add_self_to_group()
            if result2:
                return True
            else:
                return False
        return False

    def add_self_to_group(self):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        group_info = self.get_group_info(self.group_name)
        group_id = eval(group_info)[0]
        sql_stm = "insert into group_to_user(group_user_id,group_group_id) values({},{})"\
            .format(self.admin_id, group_id)
        result = db.exc_sql(sql_stm)
        return result

    def del_group(self):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "delete from group_info where group_admin_id={} and group_name='{}'"\
            .format(self.admin_id, self.group_name)
        result = db.exc_sql(sql_stm)
        return result

    @classmethod
    def get_group_info(cls, group_name):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group_id,group_admin_id,group_name from group_info where group_name='{}'".format(group_name)
        result = db.get_res(sql_stm)
        if result:
            return result[0].__str__()
        else:
            return ""

    @classmethod
    def id_to_name(cls, group_id):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group"


if __name__ == "__main__":
    print("登录测试：")
    user_name = input("请输入账户（用户名、邮箱、手机号）：")
    user_password = input("请输入密码：")
    user = User(user_name, user_password)
    r = user.login()
    if r:
        print("登录成功！您的用户ID是：{}".format(user.id))
    else:
        print("登录失败！")

    print("创建群测试：")
    group_name = input("请输入群名称：")
    group = Group(user.id, group_name)
    r = group.create_group()
    if r:
        print("创建成功！")
    else:
        print("创建失败！")

    print("解散群测试：")
    group_name = input("请输入群名称：")
    group = Group(user.id, group_name)
    r = group.del_group()
    if r:
        print("解散成功！")
    else:
        print("解散失败！")
