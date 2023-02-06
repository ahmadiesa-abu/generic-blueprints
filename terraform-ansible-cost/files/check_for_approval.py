import requests
from requests.auth import HTTPBasicAuth

from cloudify import ctx
from cloudify.exceptions import (NonRecoverableError, OperationRetry)
from cloudify.state import ctx_parameters as inputs

servicenow_host = inputs['servicenow_host']
requested_item_number = inputs['requested_item_number']
username = inputs['username']
password = inputs['password']

if requested_item_number:

    URL = "https://"+servicenow_host+"/api/now/table/sc_req_item"
    PARAMS = {
        "number": requested_item_number
    }
    AUTH = HTTPBasicAuth(username, password)

    r = requests.get(url = URL,
                     params = PARAMS, auth=AUTH)

    result = r.json()
    requested_item_document_id = result.get('result', [])[0].get('sys_id')
    PARAMS = {
        "document_id": requested_item_document_id
    }
    URL = URL.replace('sc_req_item', 'sysapproval_approver')
    r = requests.get(url = URL, params = PARAMS, auth=AUTH)

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
