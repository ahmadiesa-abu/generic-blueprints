from cloudify import ctx
from cloudify.exceptions import (NonRecoverableError, OperationRetry)
from cloudify.state import ctx_parameters as inputs

tmp_file_location = inputs['tmp_file_location']

if tmp_file_location:
    content = ''
    with open(tmp_file_location, 'r') as f:
        content = f.read()
    ctx.instance.runtime_properties['content'] = content
    if content.strip()=='stop':
        raise NonRecoverableError('File has stop content')