from cloudify.workflows import ctx

from cloudify.manager import get_rest_client

client = get_rest_client()
tenant_users = client.tenants.get(ctx.tenant_name, _get_data=True).users
ctx.logger.info('tenant_users {0}'.format(tenant_users))