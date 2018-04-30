import json
from BokeYuan import BoKeYuan

app = BoKeYuan(file=__file__)

@app.log(log=True)
@app.auth
def pages(page):
    """# 3，4，5，6写到了一个函数里，因为只是页面page不一样；并且它们需要有日志功能"""
    print("Welcome \033[1;36m%s\033[0m to \033[1;36m%s\033[0m page!" % (app.username, page))

@app.home(headBar=True)
def home():
    """导航栏的显示"""
    return ["-".join((str(index), value)) for index, value in app.func.items()]

@app.count
@app.login
def login(page):
    """login用来实现用户登录和用户注册，返回一个计算登录次数；count根据登录次数返回一个True和False，在主循环里赋给flag"""
    with open("user.txt", encoding="utf-8", mode="r") as f:  # 读取文本
        user = [json.loads(line) for line in f.readlines()]
    return page, user
# 退出程序和注销写到了一个函数里
@app.logout
@app.auth
def logout(page):
    return page

if __name__ == '__main__':
    # page和序号写在了BoKeYuan里
    app.run()



# 博客园: http://www.cnblogs.com/kuaizifeng/p/8876619.html