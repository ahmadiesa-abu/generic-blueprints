import requests
from requests.auth import HTTPBasicAuth

from cloudify import ctx
from cloudify.exceptions import (NonRecoverableError, OperationRetry)
from cloudify.state import ctx_parameters as inputs

requested_item_number = inputs['requested_item_number']
username = inputs['username']
password = inputs['password']

if requested_item_number:

    URL = "https://dev95631.service-now.com/api/now/table/{tableName}"
    PARAMS = {
        "number": requested_item_number
    }
    AUTH = HTTPBasicAuth(username, password)

    r = requests.get(url = URL.format(tableName="sc_req_item"),
                     params = PARAMS, auth=AUTH)

    result = r.json()
    requested_item_document_id = result.get('result', [])[0].get('sys_id')
    PARAMS = {
        "document_id": requested_item_document_id
    }
    r = requests.get(url = URL.format(tableName="sysapproval_approver"),
                     params = PARAMS, auth=AUTH)

    result = r.json()
    if len(result.get('result', []))>0:
        approval_state = result.get('result', [])[0].get('state')
        if approval_state not in ('rejected', 'approved'):
            raise OperationRetry('Not approved yet , trying again',
                                 retry_after=30)
        elif approval_state == 'rejected':
            raise NonRecoverableError('Request was rejected')
    else:
        raise OperationRetry('Not approved yet , trying again',
                             retry_after=30)
