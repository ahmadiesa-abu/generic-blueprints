import os
import tempfile
from cloudify import ctx
import subprocess

dep_dir = ctx.local_deployment_workdir()

with tempfile.NamedTemporaryFile(suffix=".sh",
                                 delete=False,
                                 mode="w",
                                 dir=dep_dir) as f:
    f.write('echo hello')
    f.close()
os.system('chmod u+x {0}'.format(f.name))

dep_dir = ctx.local_deployment_workdir()
result = subprocess.run(
    ['ls', '-l'],
    capture_output = True, # Python >= 3.7 only
    text = True, # Python >= 3.7 only
    cwd=dep_dir
)
ctx.logger.info('*************BEFORE*************')
ctx.logger.info('out {0}, error {1}'.format(result.stdout, result.stderr))