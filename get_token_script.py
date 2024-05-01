import requests
import sys


def login(username, password):
    # 登录的URL
    login_url = 'http://sx.bymu.cn/api/sys/manage/login'

    # 登录所需的数据
    login_data = {
        'username': username,
        'password': password,
        'schoolId': '2545'  # 学校ID固定为2545
    }

    # 发送POST请求
    response = requests.post(login_url, data=login_data)

    # 检查响应状态码
    if response.status_code == 200:
        print("登录成功！")
        # 提取token
        token = response.json().get('token')
        print("token:", token)

        # 为每个用户创建或覆盖一个Token文件
        token_filename = f'token_{username}.txt'
        with open(token_filename, 'w') as token_file:
            token_file.write(token)
        return token
    else:
        print(f"登录失败，状态码：{response.status_code}")
        return None


if __name__ == "__main__":
    # 从命令行参数获取用户名和密码
    if len(sys.argv) != 3:
        print("请提供用户名和密码作为命令行参数。")
    else:
        username = sys.argv[1]
        password = sys.argv[2]

        # 执行登录函数并获取Token
        token = login(username, password)

        # 将Token打印出来
        if token:
            print(f"Token: {token}")
        else:
            print("未能获取Token。")
