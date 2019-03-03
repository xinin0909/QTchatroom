from db_util import DBUtil
from user_info import User


class GroupUser(object):
    def __init__(self, user_id, group_name):
        self.user_id = user_id
        self.group_name = group_name
        self.group_id = None

    def add_group(self):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        group_id = self.group_name_to_id(self.group_name)
        if group_id:
            self.group_id = group_id
            sql_stm = "insert into group_to_user(group_user_id,group_group_id) values({},{})" \
                .format(self.user_id, self.group_id)
            result = db.exc_sql(sql_stm)
            return result
        else:
            return False

    def quit_group(self):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        group_id = self.group_name_to_id(self.group_name)
        if group_id:
            self.group_id = group_id
            sql_stm = "delete from group_to_user where group_user_id={} and group_group_id={}"\
                .format(self.user_id, self.group_id)
            result = db.exc_sql(sql_stm)
            return result
        else:
            return False

    @staticmethod
    def group_name_to_id(group_name):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group_id from group_info where group_name='{}'".format(group_name)
        result = db.get_res(sql_stm)
        if result:
            return result[0][0]
        else:
            return None

    @classmethod
    def get_group_info(cls, group_id):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group_id,group_admin_id,group_name from group_info where group_id={}"\
            .format(group_id, group_id)
        result = db.get_res(sql_stm)
        if result:
            return result[0].__str__()
        else:
            return ""

    @classmethod
    def get_group_list(cls, group_user_id):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group_group_id from group_to_user where group_user_id={}".format(group_user_id)
        result = db.get_res(sql_stm)
        group_list = []
        if result:
            for group_id in result:
                group_list.append(group_id[0])
        return group_list

    @classmethod
    def get_all_user_id(cls, group_group_id):
        db = DBUtil()
        db.connect_db()
        db.cur_db()
        sql_stm = "select group_user_id from group_to_user where group_group_id={}".format(group_group_id)
        result = db.get_res(sql_stm)
        group_user_list = []
        for group_user in result:
            group_user_list.append(group_user[0])
        return group_user_list


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

    print("加群测试：")
    group_name = input("请输入群名称：")
    group_user = GroupUser(user.id, group_name)
    r = group_user.add_group()
    if r:
        print("加入成功！")
    else:
        print("加入失败！")

    print("退群测试：")
    group_name = input("请输入群名称：")
    group_user = GroupUser(user.id, group_name)
    r = group_user.quit_group()
    if r:
        print("退群成功！")
    else:
        print("退群失败！")
