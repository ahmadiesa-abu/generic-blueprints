import base64

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

if __name__ == '__main__':
    username = inputs.get('username')
    password = inputs.get('password')

    encoded_userpass = "{0}:{1}".format(username, password).encode('utf-8')

    ctx.instance.runtime_properties['auth_token'] = \
        base64.b64encode(encoded_userpass).decode('utf-8')
