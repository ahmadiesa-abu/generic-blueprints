import subprocess

from cloudify import ctx
from cloudify.manager import get_rest_client
# from cloudify.utils import get_execution_token, get_rest_token, get_edge_estate_token, _get_current_context

# backup values
# execution_token = get_execution_token()
# rest_token = get_rest_token()
# edge_state_token = get_edge_estate_token()

# current_context = _get_current_context()
# if edge_state_token:
#     admin_token = ''
#     with open('/opt/mgmtworker/work/admin_token') as f:
#         admin_token = f.read()
#         #ctx.logger.info('admin_token {0}'.format(admin_token))
#     current_context._context['edge_estate_token'] = None
#     current_context._context['rest_token'] = admin_token
#     current_context._context['execution_token'] = None

version = get_rest_client().manager.get_version()['version']
ctx.logger.info('version {0}'.format(version))


# nodes = get_rest_client().nodes.list(deployment_id=ctx.deployment.id)
# for node in nodes:
#     ctx.logger.info('nodes {0}'.format(node))
# return stuff back
# if edge_state_token:
#     current_context._context['edge_estate_token'] = edge_state_token
#     current_context._context['rest_token'] = rest_token
#     current_context._context['execution_token'] = execution_token