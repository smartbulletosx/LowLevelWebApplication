import socket

URLS = {
    '/': 'hello, index',
    '/blog': 'hello, blog'
}


def pars_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    try:
        url = parsed[1]
        print(url)
        return method, url
    except:
        print(parsed[0])
    return method, '/'


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if not url in URLS:
        return 'HTTP/1.1 404 Not Found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not Found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method NOt Allowed</p>'

    return '<h1>{}</h1>'.format(URLS[url])


def generate_response(request):
    method, url = pars_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создание серверного сокета
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                             1)  # настройка сокета для многоразового использования
    server_socket.bind(('localhost', 5000))  # биндим сокет
    server_socket.listen()  # слушаем порт

    while True:
        client_socket, addr = server_socket.accept()  # принимаем клиента
        request = client_socket.recv(1024)  # принимаем данные от клиента
        print(request.decode('utf-8'))  # печатаем данные
        print()
        print(addr)  # песатаем клиента

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)  # отправяем сообщения всем клиентам в байтах
        client_socket.close()  # закрывем соединение


if __name__ == '__main__':
    run()
