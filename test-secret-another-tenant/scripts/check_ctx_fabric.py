from cloudify import ctx

from cloudify import manager

cfy_client = manager.get_rest_client()

ctx.logger.info('secret {0}'.format(cfy_client.secrets.get(ctx.node.properties.get('secert_name'))))