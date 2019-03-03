from db_util import DBUtil
from user_info import User
from friend_group import FriendGroup


class Friend(object):
    def __init__(self, user_id, friend_name, remark_name="", friend_type=1):
        self.user_id = user_id
        self.friend_name = friend_name
        self.remark_name = remark_name
        self.friend_type = friend_type
        self.friend_group = self.get_init_group_id(self.user_id)
        self.friend_id = self.find_id()

    def find_id(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select user_id from user_info where user_name='{}'".format(self.friend_name)
        result = db.get_res(sql_stm)
        if result:
            return result[0][0]
        else:
            return None

    @staticmethod
    def get_init_group_id(friend_group_user_id):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select friend_group_id from friend_group where friend_group_name='{}' " \
                  "and friend_group_user_id={}".format("我的好友", friend_group_user_id)
        result = db.get_res(sql_stm)
        if result:
            return result[0][0]
        else:
            return "null"

    def add_friend(self):
        if self.friend_id is None or self.friend_id == self.user_id:
            return False
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "insert into friendship_info(friendship_user_id,friendship_friend_id," \
                  "friendship_name,friendship_friend_type_id,friendship_friend_group_id) " \
                  "values({},{},'{}',{},{}),({},{},'',1,{})"\
            .format(self.user_id, self.friend_id, self.remark_name, self.friend_type, self.friend_group,
                    self.friend_id, self.user_id, self.get_init_group_id(self.friend_id))
        result = db.exc_sql(sql_stm)
        return result

    def del_friend(self):
        if self.friend_id is None or self.friend_id == self.user_id:
            return False
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "delete from friendship_info where (friendship_user_id={} and friendship_friend_id={}) or "\
                  "(friendship_user_id={} and friendship_friend_id={})"\
            .format(self.user_id, self.friend_id, self.friend_id, self.user_id)
        result = db.exc_sql(sql_stm)
        return result

    def set_remark_name(self, remark_name):
        self.remark_name = remark_name
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update friendship_info set friendship_name='{}' where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.remark_name, self.user_id, self.friend_id)
        result = db.exc_sql(sql_stm)
        return result

    def get_remark_name(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select friendship_name from friendship_info where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.user_id, self.friend_id)
        result = db.get_res(sql_stm)
        self.remark_name = result[0][0]
        return self.remark_name

    def set_group(self, group_id):
        self.friend_group = group_id
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update friendship_info set friendship_friend_group_id={} where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.friend_group, self.user_id, self.friend_id)
        result = db.exc_sql(sql_stm)
        return result

    def get_group(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select friendship_friend_group_id from friendship_info where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.user_id, self.friend_id)
        result = db.get_res(sql_stm)
        if result:
            self.friend_group = result[0][0]
        else:
            self.friend_group = "null"
        return self.friend_group

    def set_friend_type(self, friend_type):
        self.friend_type = friend_type
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update friendship_info set friendship_friend_type_id={} where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.friend_type, self.user_id, self.friend_id)
        result = db.exc_sql(sql_stm)
        return result

    def get_friend_type(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select friendship_friend_type_id from friendship_info where friendship_user_id={} and " \
                  "friendship_friend_id={}".format(self.user_id, self.friend_id)
        result = db.get_res(sql_stm)
        self.friend_type = result[0][0]
        return self.friend_type

    @classmethod
    def get_all_friend(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select friendship_friend_id,friendship_friend_group_id from friendship_info " \
                  "where friendship_user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        friend_dict = {}
        for friend in result:
            friend_group_name = FriendGroup.get_friend_group_name(friend[1])
            friend_name = User.id_to_name(friend[0])
            if friend_group_name not in friend_dict:
                friend_dict[friend_group_name] = []
            friend_dict[friend_group_name].append(friend_name)
        return friend_dict.__str__()

    @classmethod
    def get_friend_list(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select friendship_friend_id,friendship_name from friendship_info " \
                  "where friendship_user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        friend_list = []
        for friend in result:
            friend_mark_name = User.id_to_name(friend[0])
            friend_list.append((friend[0], friend_mark_name, friend[1]))
        return str(friend_list)

    @classmethod
    def get_friend_id_list(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select friendship_friend_id from friendship_info where friendship_user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        friend_id_list = []
        for friend_id in result:
            friend_id_list.append(friend_id[0])
        return str(friend_id_list)


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

    print("加好友测试：")
    friends_name = input("请输入要添加好友的名称：")
    friendship = Friend(user.id, friends_name)
    r = friendship.add_friend()
    if r:
        print("添加成功！")
    else:
        print("添加失败！")

    # print("删除好友测试：")
    # friends_name = input("请输入要删除的好友的名称：")
    # friendship = Friend(user.id, friends_name)
    # r = friendship.del_friend()
    # if r:
    #     print("删除成功！")
    # else:
    #     print("删除失败！")

    # print("好友备注名测试：")
    # friends_name = input("请输入好友名称：")
    # friends_nick_name = input("请输入好友备注名称：")
    # friendship = Friend(user.id, friends_name)
    # print(friendship.get_remark_name())
    # friendship.set_remark_name(friends_nick_name)
    # print(friendship.get_remark_name())

    # print("好友类别测试：")
    # friends_name = input("请输入好友名称：")
    # friends_type = int(input("请输入好友类别："))
    # friendship = Friend(user.id, friends_name)
    # print(friendship.get_friend_type())
    # friendship.set_friend_type(friends_type)
    # print(friendship.get_friend_type())

    print("获取所有好友测试：")
    # print(Friend.get_all_friend(user.id))
    d = eval(Friend.get_friend_list(user.id))
    print(d)

    # print("获取所有好友列表测试：")
    # print(FriendGroup.get_all_group(user.id))
