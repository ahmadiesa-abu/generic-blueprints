import sys
PY2 = sys.version_info[0] == 2

import copy
import time
import json
import requests

from cloudify import ctx

if PY2:
    import httplib
else:
    import http.client as httplib

def authorize_with_azure(azure_tenant, azure_client_id, azure_secret):

    url = "https://login.microsoftonline.com/{0}/oauth2/token".format(
        azure_tenant)
    body = {
        "resource" : "https://management.core.windows.net/",
        "client_id" : azure_client_id,
        "grant_type" : "client_credentials",
        "client_secret" : azure_secret
    }
    response = requests.post(url, data=body)
    return response.json()


def list_resource_groups(azure_tenant, azure_client_id, azure_secret, azure_subscription_id):
    azure_subscription_id = ctx.node.properties.get('azure_subscription_id', None)
    url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups?api-version=2022-09-01".format(
            subscriptionId = azure_subscription_id,
        )
    bearer_token = authorize_with_azure(azure_tenant, azure_client_id, azure_secret).get('access_token', 'invalid_creds')
    if bearer_token == 'invalid_creds':
        return 401, "Invalid Token -it wasn't created-"
    headers = {
        'Authorization': 'Bearer ' + authorize_with_azure(azure_tenant, azure_client_id, azure_secret)['access_token'],
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()



azure_tenant = ctx.node.properties.get('azure_tenant_id', None)
azure_client_id = ctx.node.properties.get('azure_client_id', None)
azure_secret = ctx.node.properties.get('azure_client_secret', None)
azure_subscription_id = ctx.node.properties.get('azure_subscription_id', None)


if azure_tenant is None or azure_client_id is None or azure_secret is None or azure_subscription_id is None:
    ctx.instance.runtime_properties['connection_status'] = 'Invalid Credentials'
    ctx.instance.runtime_properties['debug_action'] = 'Check your input values'

else:

    status_code, response_content = list_resource_groups(azure_tenant, azure_client_id, azure_secret, azure_subscription_id)

    if status_code != 200:
        ctx.instance.runtime_properties['connection_status'] = 'Invalid Credentials'
        ctx.instance.runtime_properties['debug_action'] = 'Check your input values'
        ctx.instance.runtime_properties['http_response'] = response_content
    else:
        ctx.instance.runtime_properties['connection_status'] = 'Valid Credentials'
        ctx.instance.runtime_properties['http_response'] = response_content

