import json
from cloudify import ctx


downloaded_file = ctx.download_resource(ctx.node.properties.get('node_runtime_json_file'))
ctx.logger.info('downloaded file path : {0}'.format(downloaded_file))
download_json_content = ''
with open(downloaded_file, 'r') as f:
    download_json_content = f.read()

runtime_properties = json.loads(download_json_content)

ctx.instance.runtime_properties = runtime_properties
ctx.instance.update()
# I know dump , but to expose it :) as generic value
ctx.instance.runtime_properties['runtime_properties'] = runtime_properties
