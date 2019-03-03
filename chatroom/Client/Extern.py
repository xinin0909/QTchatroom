# 用来存储一些常量或者简单的数据结构什么的


# 用户信息索引
class FriendInfoIndex:
    obj_type = 0
    id = 1  # id索引
    name = 2  # 用户名索引
    nick_name = 3  # 昵称索引
    phone = 4
    mail = 5
    gender = 6
    age = 7
    birthday = 8
    vocation = 9
    signature = 10
    register_time = 11
    mark_name = 12  # 备注索引


# 群信息索引
class GroupIndexInfo:
    obj_type = 0
    group_id = 1
    group_admin_id = 2
    group_name = 3


# 用户信息
class UserInfo:
    def __init__(self, obj_type, uid="", name="", nick_name="", phone="", mail="", gender=3, age=0,
                 birthday="", vocation="", signature="", register_time="", mark_name=""):
        self.obj_type = obj_type  # 对象类型，0为好友，1为群
        self.id = uid  # 用户id
        self.name = name  # 用户名
        self.nick_name = nick_name  # 用户备注名或昵称
        self.phone = phone  # 用户电话
        self.mail = mail  # 用户邮箱
        self.gender = gender  # 用户性别 1为男，2为女，3为保密
        self.age = age  # 用户年龄
        self.birthday = birthday  # 用户生日
        self.vocation = vocation  # 用户职业
        self.signature = signature  # 用户签名
        self.register_time = register_time  # 用户注册时间
        self.mark_name = mark_name  # 用户备注名


# 群信息
class GroupInfo:
    def __int__(self, group_id="", group_admin_id="", group_name=""):
        self.obj_type = 1
        self.group_id = group_id
        self.group_admin_id = group_admin_id
        self.group_name = group_name
