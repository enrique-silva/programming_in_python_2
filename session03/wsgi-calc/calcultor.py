from wsgiref.simple_server import make_server
import random

home_page = """<h1>This is a simple calculator</h1>
<ol>
<li> To perform any calculation to the end of the URL http://localhost:8080/operation_type/number1/number2
<li> Operations we support: multiply, add, subtract, divide
<li> Hit enter
<li> Voila! Find your answer below
</ol>
<p> For example, to find what 13 + 7 equals your URL would look like this:</p>
<p> http://localhost:8080/add/13/7
<h1>Current Answer: {answer} </h1>"""


def add(*args):
    answer = int(args[0]) + int(args[1])
    return str(answer)


def subtract(*args):
    answer = int(args[0]) - int(args[1])
    return str(answer)


def multiply(*args):
    answer = int(args[0]) * int(args[1])
    return str(answer)


def divide(*args):
    try:
        answer = int(args[0]) / int(args[1])
    except:
        raise ZeroDivisionError
    return str(answer)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        answer = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        answer = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        answer = "<h1>Internal Server Error</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        answer = "<h1>Division by Zero is not allowed</h1>"
    finally:
        body = home_page.format(answer=answer)
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    args = path.strip('/').split('/')
    func_name = args.pop(0)
    func ={
        "multiply" : multiply,
        "add"      : add,
        "divide"   : divide,
        "subtract" : subtract,
    }.get(func_name)
    return func, args


if __name__ == '__main__':
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()