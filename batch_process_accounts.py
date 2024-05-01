import subprocess
import requests

def send_pushplus_notification(token, title, content):
    pushplus_url = f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'
    response = requests.get(pushplus_url)
    return response

# 替换为您的PushPlus Token
pushplus_token = '0cb6ae2cca62498182697216da27967a'

# 打开包含多个账号信息的文件，每行一个账号，格式为：用户名 密码 经度 纬度
with open('accounts.txt', 'r') as accounts_file:
    for line in accounts_file:
        account_info = line.strip().split()
        username, password, lat, lng = account_info

        # 运行获取Token的脚本，并将用户名和密码传递给它
        get_token_script = f"python get_token_script.py {username} {password}"
        token_process = subprocess.Popen(get_token_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        token_process.wait()

        # 检查是否有错误输出
        token_error = token_process.stderr.read().decode().strip()
        if token_error:
            notification_content = f"获取Token时出现错误 ({username}): {token_error}"
            print(notification_content)
            send_pushplus_notification(pushplus_token, 'Token获取错误', notification_content)
        else:
            print(f"Token获取成功 ({username}).")

            # 运行签到脚本，传递用户名、经度和纬度
            sign_script = f"python sign_script.py {username} {lat} {lng}"
            sign_process = subprocess.Popen(sign_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sign_process.wait()

            # 检查是否有错误输出
            sign_error = sign_process.stderr.read().decode().strip()
            if sign_error:
                notification_content = f"签到时出现错误 ({username}): {sign_error}"
                print(notification_content)
                send_pushplus_notification(pushplus_token, '签到错误', notification_content)
            else:
                sign_output = sign_process.stdout.read().decode().strip()
                notification_content = f"开始签到 ({username}): {sign_output}"
                print(notification_content)
                send_pushplus_notification(pushplus_token, '签到结果', notification_content)
