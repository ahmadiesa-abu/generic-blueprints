import json
from cloudify import ctx


def return_b(a, b):
    ctx.logger.info('a {0}'.format(json.dumps(a)))
    ctx.logger.info('b {0}'.format(json.dumps(b)))
    return b

try:
    ctx.instance.runtime_properties['a_list'].append(1)
    ctx.instance.runtime_properties['a_dict'].update({
        'key1': 'value1'
    })
    # if we call internal method _set_changed it will work 
    #ctx.instance.runtime_properties._set_changed()
    # if we use the conflict method it will work [ given that we return second arg , which is the latest_properties ]
    #ctx.instance.update(return_b)
    # calling update won't do anything
    #ctx.instance.update()
except Exception as e:
    ctx.logger.error(str(e))