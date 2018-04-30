import functools, importlib, sys, json, time


class BoKeYuan(object):
    """define a class decoration for the after BoKeYuan handlers."""
    def __init__(self, file, appname="jingyu", username=False):
        self.func = {1: "login", 2: "register", 3: "article", 4: "diary", 5: "comment", 6: "collect", 7: "logout", 8: "exit"}
        self.myfunc = {1: "login", 2: "login", 3: "pages", 4: "pages", 5: "pages", 6: "pages", 7: "logout", 8: "exit"}
        self.dict = {}
        self.username = username
        self.app = appname
        self.file = file.split("/")[-1].split(".")[0]
        importlib.import_module(self.file)  # 导入文件对象并执行函数.

    def __call__(self, *args, **kwargs):pass  # 应该写在这里，它是框架的入口
    # 用户登录装饰器，把装饰的函数名字写到self.dict里
    def auth(self, f):
        @functools.wraps(f)
        def decorator(*args, **kwargs):
            self.dict["user"] = f.__name__
            if self.username:
                f(*args, **kwargs)
                return True, args  # 这个地方得返回page的参数，在退出或注销程序时用的上
            else:
                print("Please login first!")
                return False, args
        return decorator

    # 生成日志装饰器，把装饰的函数名字写到self.dict里
    def log(self, log=True):  # 装饰器，用来开启日志功能
        def decorator(f):
            @functools.wraps(f)
            def fn(*args, **kwargs):
                flag, page = f(*args, **kwargs)
                if flag:
                    timer = time.strftime("%Y-%m-%d", time.localtime())
                    string = "用户:%s 在%s 执行了 %s函数" % (self.username, timer, page[0])  # 这里要存入到日志文件
                    with open("log.txt", encoding="utf-8", mode="a") as file:
                        file.write(string + "\n", )
                else:
                    pass
                self.dict["log"] = f.__name__
            return fn
        return decorator
    # 首页展示装饰器，把装饰的函数名字写到self.dict里
    def home(self, headBar=True):
        def decorator(f):
            @functools.wraps(f)
            def fn(*args, **kwargs):
                if headBar:
                    title = " " * 38 + "欢迎来到博客园" + " " * 38
                    print("\033[1;36m%s\033[0m" % title)
                    print("\033[1;36m%s\033[0m" % ("-" * len(title)))
                    head = f(*args, **kwargs)
                    print("\033[1;36m  %s\033[0m" % (" %s " * len(head) % tuple(head)))
                    print("\033[1;36m%s\033[0m" % ("-" * len(title)))
                self.dict["home"] = f.__name__
            return fn
        return decorator
    def login(self, f):  # 装饰器，用来进行用户登录和用户注册判断
        @functools.wraps(f)
        def decorator(*args, **kwargs):
            page, user_passwd = f(*args, **kwargs)
            count = 0
            while True:
                if count >= 3:
                    print("times out!");break
                if not self.username:
                    username = input("-请输入登陆账号: ")
                    password = input("-请输入登陆密码: ")
                    if page == "login":
                        # 如果是登录且验证成功
                        if {"username": username, "password": password} in user_passwd:# 如果用户名和密码都在user_list表里
                            self.username = username
                            print("欢迎\033[1;36m %s \033[0m登录！" % username);break
                        # 如果是登录但未验证成功
                        else:
                            print("username or password not correct!")
                            count += 1
                            if count >= 3:
                                print("password not same!");break
                    else:
                        # 如果是注册，则需要验证用户名是否已存在
                        user_list = [dic["username"] for _, dic in enumerate(user_passwd)]
                        if username in user_list:
                            print("用户名已存在！请重新输入！")
                            count += 1
                        else:
                            # 如果用户名通过，则允许输入密码
                            password_again = input("-请再次输入登陆密码: ")
                            # 密码验证成功，就把用户追加写入到user表里
                            if password_again == password:
                                self.username = username  # 此时要把这个用户追加到注册表里
                                with open("user.txt", encoding="utf-8", mode="a") as file:
                                    file.write(json.dumps({"username": username, "password": password_again}) + "\n", )
                            # 密码验证失败，就计数
                            else:
                                count += 1
                                print("password again is not the same one!")
                else:
                    print("User \033[1;36m %s\033[0m has logged in！" % self.username);break
            return count
        return decorator
    def count(self, f):
        def decorator(*args, **kwargs):
            out = f(*args, **kwargs)
            if out < 3:
                return True
            else:
                return False
        return decorator

    def logout(self, f):
        @functools.wraps(f)
        def decorator(*args, **kwargs):
            flag, page = f(*args, **kwargs)
            if flag:  # 如果用户注销，且用户已登录，就需要注销用户
                print("User \033[1;36m %s \033[0m has logged out." % self.username)
                self.username = False  # 注销用户
            return True
        return decorator
    def run(self):
        flag =True
        while flag:
            getattr(sys.modules[self.file], "home")()
            number = input("\033[1;36m-请按索引选择功能键: \033[0m")
            number = int(number) if number.isdigit() and 0 <= int(number) <= 8 else False
            if number:
                if number in [3, 4, 5, 6]:  # 文章、日志、评论、收藏
                    getattr(sys.modules[self.file], "pages")(self.func[number])
                elif number != 8:
                    flag = getattr(sys.modules[self.file], self.myfunc[number])(self.func[number])
                else:
                    print("浏览器已关闭！"); break