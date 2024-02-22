import os

from cloudify import ctx

dep_dir = ctx.local_deployment_workdir()
count = 0
for root_dir, cur_dir, files in os.walk(dep_dir):
    count += len(files)
ctx.logger.info(f'file count: {count}')