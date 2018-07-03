import socket
import ssl
import re
'''
def protocol_of_url(url):

    #返回代表协议的字符串, 'http' 或者 'https'

    #创建一个socket对象
    s = socket.socket()
    host = url
    port = 80
    #连接上主机
    s.connect((host, port))
    #构建一个请求发送给服务器
    http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
    #发送前将str格式转化为bytes，编码为utf-8，使send函数可以支持
    request = http_request.encode('utf-8')
    s.send(request)
    #接收响应
    responed = s.recv(1024)
    #转码使可用正则表达式
    responed = str(responed)
    print(responed)
    #判断协议类型
    if bool(re.findall('https',responed)) == True:
        print('https')
        return 'https'
    else:
        print('http')
        return 'http'
protocol_of_url('zhihu.com')
'''
'''
# 创建一个socket对象
s = socket.socket()
host = 'huya.com'
port = 80
# 连接上主机
s.connect((host, port))
# 构建一个请求发送给服务器
http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
# 发送前将str格式转化为bytes，编码为utf-8，使send函数可以支持
request = http_request.encode('utf-8')
s.send(request)
# 接收响应
responed = s.recv(1024)
# 转码使可用正则表达式
responed = str(responed)
print(responed)
if responed[:7] == 'http://':
    print('http')
elif responed[:8] == 'https://':
    print('https')
else:
    print('aa\n',responed)
# 判断协议类型
if responed[:7] == 'http://':
    print('https')
    return 'https'
else:
    print('http')
    return 'http'
'''

def parsed_url(url):
    #检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    #检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    #检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    #默认端口
    port = port_dict[protocol]
    if ':' in host:
        u = host.split(':')
        host = u[0]
        port = int(u[1])
    return protocol,host,port,path

def socket_by_protocol(protocol):
#根据协议返回一个socket实例
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s

def response_by_socket(s):
#参数是一个socket 实例
#返回这个socket读取的所有数据
    respons = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        respons += r
    return respons

def parsed_response(r):
#把response解析出状态码headers body返回状态码是int
#headers是dict
#body是str
    header, body = r.split('\r\n\r\n',1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    statu_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k,v = line.split(': ')
        headers[k] = v
    return status_code, headers, body

def get(url):
    #用get请求url并返回响应
    protocol,host,port,path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host,port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path,host)
    s.send(request.encode('utf-8'))
    response = response_by_socket(s)
    r = response.decode('utf-8')

    status_code, headers, body = parsed_response(r)
    if status_code in [301,302]:
        url = headers['Location']
        return get(url)
    return status_code, headers,body


#test 单元测试
def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = {
        ('http://g.cn',(http,host,80,path)),
        ('http://g.cn/',(http,host,80,path)),
        ('http://g.cn:90',(http,host,90,path)),
        ('http://g.cn:90/',(http,host,90,path)),
        ('https://g.cn',(https,host,443,path)),
        ('https://g.cn:233/',(https,host,233,path)),
    }

    for t in test_items:
        url = t[0]
        expected = t[1]
        u = parsed_url(url)
        e = "parsed_url ERROR,({}) ({}) ({})".format(url,u,expected)
        #TURE则断言成功，FALSE则输出e
        assert u == expected,e

def test():
    #用于测试主函数
    test_parsed_url()


if __name__ == '__main__':
    print(get('https://zhihu.com'))
