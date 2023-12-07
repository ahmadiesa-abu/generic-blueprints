from cloudify import ctx
import subprocess

dep_dir = ctx.local_deployment_workdir()
result = subprocess.run(
    ['ls', '-l'],
    capture_output = True, # Python >= 3.7 only
    text = True, # Python >= 3.7 only
    cwd=dep_dir
)
ctx.logger.info('*************AFTER*************')
ctx.logger.info('out {0}, error {1}'.format(result.stdout, result.stderr))