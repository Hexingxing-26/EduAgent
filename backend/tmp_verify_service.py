import http.client
import json
import random
import string


def request(path, method='GET', body=None, headers=None):
    conn = http.client.HTTPConnection('127.0.0.1', 8000, timeout=10)
    if headers is None:
        headers = {}
    if body is not None and 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'
    conn.request(method, path, body, headers)
    resp = conn.getresponse()
    data = resp.read().decode('utf-8', errors='replace')
    conn.close()
    return resp.status, dict(resp.getheaders()), data

print('root test')
status, headers, body = request('/')
print(status, body)

name = 'autotest_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
register_body = json.dumps({'username': name, 'password': 'Test1234', 'nickname': 'auto', 'major': '测试'})
status2, headers2, body2 = request('/user/register', 'POST', register_body)
print('register status', status2)
print('register body', body2)

try:
    register_result = json.loads(body2)
except Exception as e:
    register_result = None
    print('register parse failed', e)

if register_result and register_result.get('code') == 200:
    login_body = json.dumps({'username': name, 'password': 'Test1234'})
    status3, headers3, body3 = request('/user/login', 'POST', login_body)
    print('login status', status3)
    print('login body', body3)
else:
    print('register failed, skip login')
