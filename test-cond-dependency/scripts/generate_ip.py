import random

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


def generate_random_ip():
    ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return ip_address


if __name__ == "__main__":
    if inputs.get('some_ip', ''):
        ctx.instance.runtime_properties['ip'] = inputs.get('some_ip')
    else:
        ctx.instance.runtime_properties['ip'] = generate_random_ip()