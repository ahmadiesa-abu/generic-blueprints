from cloudify import ctx

for rel in ctx.instance.relationships:
    ctx.logger.info('rel.type {0}'.format(rel.type))