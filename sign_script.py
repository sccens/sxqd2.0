import requests
import uuid
import sys

def sign_in_with_token_and_location(username, lat, lng):
    # 从特定文件读取Token
    token_filename = f'token_{username}.txt'
    try:
        with open(token_filename, 'r') as file:
            token = file.read().strip()
    except FileNotFoundError:
        print(f"未找到用户 {username} 的Token文件。")
        return "未找到Token文件"

    headers = {
        'Token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    data = {
        'lat': lat,
        'lng': lng,
        'phoneUuid': uuid.uuid4().hex,
        'taskId': '89',
        'type': '1',
    }
    url = 'http://sx.bymu.cn/api/sign/signIn'
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    msg = response_data.get('msg')
    return msg

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("请提供用户名、经度和纬度作为命令行参数。")
    else:
        username = sys.argv[1]
        lat = sys.argv[2]
        lng = sys.argv[3]

        sign_result = sign_in_with_token_and_location(username, lat, lng)
        print("签到结果:", sign_result)
