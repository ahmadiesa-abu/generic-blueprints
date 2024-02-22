import random

from cloudify import ctx


def generate_random_ip():
    ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return ip_address


if __name__ == "__main__":
    ctx.instance.runtime_properties['ip'] = generate_random_ip()