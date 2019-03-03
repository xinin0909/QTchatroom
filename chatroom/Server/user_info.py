from hashlib import sha1
from time import time, localtime
from db_util import DBUtil
from friend_group import FriendGroup



def encrypted_password(in_password):
    s1 = sha1()
    s1.update(in_password.encode("utf8"))  # 将密码加密
    return s1.hexdigest()  # 返回加密后的密码


class User(object):
    __doc__ = '''
    该类用来创建用户
    '''

    def __init__(self, name, password, email=""):
        self.id = None    # 用户ID，非空，主键
        self.name = name    # 设置用户名，非空
        self.nick_name = None    # 用户昵称
        self.password = encrypted_password(password)    # 设置用户加密后的密码
        self.signature = None    # 用户签名
        self.gender_id = 3    # 用户性别，0为男，1为女
        self.birthday = None    # 用户生日
        self.telephone = None    # 设置用户登录手机号，非空
        self.email = email    # 设置登录邮箱，非空
        self.introduce = None    # 用户介绍
        self.head = None    # 用户头像
        self.age = None    # 用户年龄
        self.vocation = None    # 用户的职业信息
        self.nation_id = None    # 用户所属国家
        self.province_id = None    # 用户所属省
        self.city_id = None    # 用户所属城市
        self.friendship_policy_id = 1    # 用户加好友的策略，非空
        self.status_id = 1    # 用户在线状态，非空
        self.friend_policy_question = None    # 用户好友策略问题
        self.friend_policy_answer = None    # 用户好友策略答案
        self.friend_policy_password = None    # 用户好友策略密码
        self.register_time = None    # 用户注册时间，非空

    def register(self):
        __doc__ = '''
        注册用户信息
        :return: 注册是否成功
        '''
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        args = (self.name, self.password, self.email)    # 设置SQL语句参数
        sql_stm = "insert into user_info(user_name,user_password,user_email) values(%s,%s,%s)"
        result = db.exc_sql(sql_stm, *args)
        if result:
            self.get_user_id()
            friend_group = FriendGroup(self.id)
            friend_group.add_friend_group()

        return result

    def get_user_id(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        args = (self.name, )
        sql_stm = "select user_id from user_info where user_name=%s"
        result = db.get_res(sql_stm, *args)
        if result:
            self.id = result[0][0]
        else:
            self.id = None
        return self.id

    def login(self):
        __doc__ = '''
        用户登录
        :return: 登录是否成功
        '''
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        args = (self.password, self.name, self.name, self.name)    # 设置SQL语句参数
        sql_stm = "select user_id from user_info where (user_password=%s and " \
                  "(user_name=%s or user_email=%s or user_telephone=%s))"
        result = db.get_res(sql_stm, *args)  # 执行SQL语句
        if result:
            self.id = result[0][0]
            self.get_inf()
            return self.id    # 获取用户ID
        else:
            return None

    def get_inf(self):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "select user_name,user_nick_name,user_signature,user_gender_id,user_birthday," \
                  "user_telephone,user_email,user_introduce,user_head,user_age,user_vocation," \
                  "user_nation_id,user_province_id,user_city_id,user_register_time " \
                  "from user_info where user_id={}".format(self.id)
        result = db.get_res(sql_stm)
        self.name = result[0][0]
        self.nick_name = result[0][1]  # 用户昵称
        self.signature = result[0][2]  # 用户签名
        self.gender_id = result[0][3]  # 用户性别，0为男，1为女
        self.birthday = result[0][4]  # 用户生日
        self.telephone = result[0][5]  # 设置用户登录手机号，非空
        self.email = result[0][6]  # 设置登录邮箱，非空
        self.introduce = result[0][7]  # 用户介绍
        self.head = result[0][8]  # 用户头像
        self.age = result[0][9]  # 用户年龄
        self.vocation = result[0][10]  # 用户的职业信息
        self.nation_id = result[0][11]  # 用户所属国家
        self.province_id = result[0][12]  # 用户所属省
        self.city_id = result[0][13]  # 用户所属城市
        self.register_time = result[0][14]  # 用户注册时间，非空
        # print(self.register_time.date())

    def set_inf(self, nick_name="", signature="", gender_id=3, birthday=None, telephone="", email="",
                introduce="", head="", age=0, vocation="", nation_id=1, province_id=1, city_id=1):
        self.nick_name = nick_name    # 用户昵称
        self.signature = signature    # 用户签名
        self.gender_id = gender_id    # 用户性别，0为男，1为女
        self.birthday = birthday    # 用户生日
        self.telephone = telephone    # 设置用户登录手机号，非空
        self.email = email    # 设置登录邮箱，非空
        self.introduce = introduce    # 用户介绍
        self.head = head    # 用户头像
        self.age = age    # 用户年龄
        self.vocation = vocation    # 用户的职业信息
        self.nation_id = nation_id    # 用户所属国家
        self.province_id = province_id    # 用户所属省
        self.city_id = city_id    # 用户所属城市
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update user_info set user_nick_name='{}',user_signature='{}',user_gender_id={}," \
                  "user_birthday='{}',user_telephone='{}',user_email='{}',user_introduce='{}',user_head='{}'," \
                  "user_age={},user_vocation='{}',user_nation_id={},user_province_id={},user_city_id={} " \
                  "where user_name='{}'".format(self.nick_name, self.signature, self.gender_id, self.birthday,
                                                self.telephone, self.email, self.introduce, self.head, self.age,
                                                self.vocation, self.nation_id, self.province_id, self.city_id,
                                                self.name)
        result = db.exc_sql(sql_stm)
        return result

    def update_password(self, old_password, new_password):
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        args = (encrypted_password(new_password), self.name, encrypted_password(old_password))
        sql_stm = "update user_info set user_password=%s where (user_name=%s and user_password=%s)"
        result = db.exc_sql(sql_stm, *args)
        return result

    def set_friend_policy(self, friendship_policy_id):
        self.friendship_policy_id = friendship_policy_id
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update user_info set user_friendship_policy_id={} " \
                  "where user_name='{}'".format(self.friendship_policy_id, self.name)
        return db.exc_sql(sql_stm)

    def get_friend_policy(self):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select user_friendship_policy_id from user_info " \
                  "where user_name='{}'".format(self.name)
        result = db.get_res(sql_stm)
        if result:
            self.friendship_policy_id = result[0][0]
        return self.friendship_policy_id

    def set_status(self, status_id):
        self.status_id = status_id
        db = DBUtil()    # 创建数据库对象
        db.connect_db()    # 创建连接对象
        db.cur_db()    # 创建游标
        sql_stm = "update user_info set user_status_id={} " \
                  "where user_name='{}'".format(self.status_id, self.name)
        return db.exc_sql(sql_stm)

    def get_status(self):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select user_status_id from user_info " \
                  "where user_name='{}'".format(self.name)
        result = db.get_res(sql_stm)
        if result:
            self.status_id = result[0][0]
        return self.status_id

    @classmethod
    def id_to_name(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "select user_name from user_info where user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        if result:
            out_user_name = result[0][0]
        else:
            out_user_name = None
        return out_user_name

    @classmethod
    def name_to_id(cls, in_user_name):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        args = (in_user_name, in_user_name, in_user_name)  # 设置SQL语句参数
        sql_stm = "select user_id from user_info where " \
                  "(user_name=%s or user_email=%s or user_telephone=%s)"
        result = db.get_res(sql_stm, *args)
        if result:
            out_user_id = result[0][0]
        else:
            out_user_id = None
        return out_user_id

    @classmethod
    def get_user_info(cls, in_user_id):
        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        user_info_dict = dict()
        sql_stm = "select user_name,user_nick_name,user_signature,user_gender_id,user_birthday," \
                  "user_telephone,user_email,user_introduce,user_head,user_age,user_vocation," \
                  "user_nation_id,user_province_id,user_city_id,user_register_time " \
                  "from user_info where user_id={}".format(in_user_id)
        result = db.get_res(sql_stm)
        if result:
            user_info_dict['name'] = result[0][0]  # 用户名
            user_info_dict['nick_name'] = result[0][1]  # 用户昵称
            user_info_dict['signature'] = result[0][2]  # 用户签名
            user_info_dict['gender_id'] = result[0][3]  # 用户性别，1为男，2为女，3为保密
            if result[0][4] is None:
                user_info_dict['birthday'] = ''
                user_info_dict['age'] = 0
            else:
                user_info_dict['birthday'] = str(result[0][4])  # 用户生日
                user_info_dict['age'] = localtime(time())[0] - int(str(result[0][4]).split('-')[0])  # 用户年龄
            user_info_dict['telephone'] = result[0][5]  # 设置用户登录手机号，非空
            user_info_dict['email'] = result[0][6] # 设置登录邮箱，非空
            # self.introduce = result[0][7]  # 用户介绍bbb
            # self.head = result[0][8]  # 用户头像
            user_info_dict['vocation'] = result[0][10]  # 用户的职业信息
            # self.nation_id = result[0][11]  # 用户所属国家
            # self.province_id = result[0][12]  # 用户所属省
            # self.city_id = result[0][13]  # 用户所属城市
            user_info_dict['register_time'] = str(result[0][14].date())  # 用户注册时间，非空
        return str(user_info_dict)

    @classmethod
    def set_user_info(cls, in_user_id, user_info_dict):
        nick_name = user_info_dict['nick_name']  # 用户昵称
        signature = user_info_dict['signature']  # 用户签名
        gender_id = user_info_dict['gender_id']  # 用户性别，1为男，2为女，3为保密
        birthday = user_info_dict['birthday']  # 用户生日
        if birthday != '':
            age = user_info_dict['age'] = localtime(time())[0] - int(birthday.split('-')[0])  # 用户年龄
            birthday = "'{}'".format(birthday)
        else:
            age = 0
            birthday = 'null'
        telephone = user_info_dict['telephone']  # 设置用户登录手机号，非空
        email = user_info_dict['email']  # 设置登录邮箱，非空
        vocation = user_info_dict['vocation']  # 用户的职业信息

        db = DBUtil()  # 创建数据库对象
        db.connect_db()  # 创建连接对象
        db.cur_db()  # 创建游标
        sql_stm = "update user_info set user_nick_name='{}',user_signature='{}',user_gender_id={}," \
                  "user_birthday={},user_telephone='{}',user_email='{}'," \
                  "user_age={},user_vocation='{}' " \
                  "where user_id={}".format(nick_name, signature, gender_id, birthday, telephone, email,
                                                age, vocation, in_user_id)
        result = db.exc_sql(sql_stm)
        return result


if __name__ == "__main__":
    # print("注册测试：")
    # user_name = input("请输入用户名：")
    # user_password = input("请输入密码：")
    # user_email = input("请输入邮箱：")
    # user = User(user_name, user_password, user_email)
    # rr = user.register()
    # if rr:
    #     print("注册成功！")
    # else:
    #     print("注册失败！")

    print("登录测试：")
    user_name = input("请输入账户（用户名、邮箱、手机号）：")
    user_password = input("请输入密码：")
    user = User(user_name, user_password)
    user_id = user.login()
    if user_id:
        print("登录成功！您的用户ID是：{}".format(user.id))
    else:
        print("登录失败！")

    # print("密码修改测试：")
    # password_old = input("请输入原密码：")
    # password_new = input("请输入新密码：")
    # r = user.update_password(password_old, password_new)
    # if r:
    #     print("修改成功！")
    # else:
    #     print("修改失败！")

    print("获取用户信息测试：")
    print(user.get_user_info(user.id))

    # print("修改用户信息测试：")
    # user.set_inf(telephone="8888", email="aaa@aaa", birthday="1996-05-21")
    # user.get_inf()

    # print("修改好友策略测试：")
    # print(user.get_friend_policy())
    # user.set_friend_policy(0)
    # print(user.get_friend_policy())

    # print("修改在线状态测试：")
    # print(user.get_status())
    # user.set_status(2)
    # print(user.get_status())
