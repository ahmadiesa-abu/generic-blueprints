import os
import random
import string

from cloudify import ctx


def generate_random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


dep_dir = ctx.local_deployment_workdir()
ctx.logger.info(f'creating files inside {dep_dir}')
for i in range(1, 2001):
    file_path = os.path.join(dep_dir, f'file_{i}.txt')
    with open(file_path, 'w') as file:
        random_data = generate_random_data(100)
        file.write(random_data)

ctx.logger.info('done creating files')