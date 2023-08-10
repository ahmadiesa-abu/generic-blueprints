from cloudify import ctx
import os
# ctx.logger.info(os.listdir("/etc/cloudify/.ssh"))

# os.system('mv /etc/cloudify/.ssh/id_rsa.pub /etc/cloudify/.ssh/id_rsa.pub_bkp')

# os.system('cd /etc/cloudify/ && ssh-keygen -f /etc/cloudify/.ssh/id_rsa -t rsa -b 2048 -q -P ""')

# with open('/etc/cloudify/.ssh/id_rsa.pub', 'r') as f:
#     ctx.logger.info(f.read())

# with open('/etc/cloudify/.ssh/id_rsa', 'r') as f:
#     ctx.logger.info(f.read())

github_host = 'XXXX'

os.system('ssh-keyscan -H %s >> /etc/cloudify/.ssh/known_hosts' %github_host)