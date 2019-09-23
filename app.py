import config


connex_app = config.connex_app
connex_app.add_api('api.yml')


@connex_app.route('/')
def hello_world():
    return 'Hello world!'

def contact_read():
    return ['test_contact_read']


if __name__ == '__main__':
    connex_app.run(debug=True)
