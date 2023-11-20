import sys
import json
sys.path.insert(0, '/opt/mgmtworker/env/lib/python3.11/site-packages')
from cloudify import ctx
from cloudify.exceptions import NonRecoverableError

from cloudify_types.utils import (delete_plugins_secrets_and_runtime,
                                  errors_nonrecoverable,
                                  get_desired_operation_input,
                                  get_client, get_idd,
                                  deployment_id_exists)


downloaded_file = ctx.download_resource(ctx.node.properties.get('node_runtime_json_file'))
ctx.logger.info('downloaded file path : {0}'.format(downloaded_file))
download_json_content = ''
with open(downloaded_file, 'r') as f:
    download_json_content = f.read()

runtime_properties = json.loads(download_json_content)

if not os.isfile('/tmp/stop.txt'):
    with open('/tmp/stop.txt','w') as f:
        f.write('just for fun')
        # raise NonRecoverableError('failing you for fun')
ctx.instance.runtime_properties = runtime_properties
ctx.instance.update()
# I know dump , but to expose it :) as generic value
ctx.instance.runtime_properties['runtime_properties'] = runtime_properties
