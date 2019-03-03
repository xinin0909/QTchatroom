from db_util import DBUtil


class FriendGroup(object):
    def __init__(self, group_user_id, group_name="我的好友"):
        self.friend_group_id = None
        self.group_name = group_name
        self.group_user_id = group_user_id

    def get_friend_group_id(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select friend_group_id from friend_group where friend_group_user_id={}".format(self.group_user_id)
        result = db.get_res(sql_stm)
        if result:
            self.group_user_id = result[0][0]
        else:
            self.group_user_id = None
        return self.group_user_id

    def add_friend_group(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "insert into friend_group(friend_group_name,friend_group_user_id) " \
                  "values('{}',{})".format(self.group_name, self.group_user_id)
        result = db.exc_sql(sql_stm)
        return result

    def del_friend_group(self):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "delete from friend_group where friend_group_name='{}' and friend_group_user_id={}"\
            .format(self.group_name, self.group_user_id)
        result = db.exc_sql(sql_stm)
        return result

    def rename_group(self, new_group_name):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "update friend_group set friend_group_name='{}' where friend_group_user_id={}"\
            .format(new_group_name, self.group_user_id)
        result = db.exc_sql(sql_stm)
        return result

    @classmethod
    def get_friend_group_name(cls, in_group_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select friend_group_name from friend_group where friend_group_id={}".format(in_group_id)
        result = db.get_res(sql_stm)
        if result:
            return result[0][0]
        else:
            return None

    @classmethod
    def get_all_group(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select friend_group_name from friend_group where friend_group_user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        group_list = []
        for group in result:
            group_list.append(group[0])
        return group_list


if __name__ == "__main__":
    print("好友分组测试：")
