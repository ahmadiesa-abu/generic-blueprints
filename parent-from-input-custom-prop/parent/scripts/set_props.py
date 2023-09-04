from cloudify import ctx


ctx.instance.runtime_properties['my_test'] = 'set from script'
ctx.instance.update()