import form

# 新規作成
def application(environ, start_response):
    print('aaaa')
    html = form.init(environ, start_response)
    return html