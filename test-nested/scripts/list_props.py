from cloudify import ctx
from cloudify.state import ctx_parameters


for k,v in ctx_parameters.items():
    ctx.logger.info(f'{k} : {v}')