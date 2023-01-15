import json

from time import sleep, time
from copy import deepcopy

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client
from cloudify.exceptions import NonRecoverableError

from cloudify_rest_client.exceptions import (
    DeploymentEnvironmentCreationPendingError,
    DeploymentEnvironmentCreationInProgressError)

def convert_list_to_dict(labels):
    labels = deepcopy(labels)
    target_dict = {}
    for label in labels:
        target_dict[label['key']] = label['value']
    return target_dict


def convert_dict_to_list(labels):
    labels = deepcopy(labels)
    target_list = []
    for key, value in labels.items():
        target_list.append({key: value})
    return target_list

downloaded_file = ctx.download_resource(inputs['file_location'])
ctx.logger.info('downloaded file path : {0}'.format(downloaded_file))
file_content = ''
with open(downloaded_file, 'r') as f:
    file_content = f.read()

download_json_content = json.loads(file_content)

runtime_properties = download_json_content.get('runtime_properties', {})
ctx.instance.runtime_properties = runtime_properties
ctx.instance.update()
rest_client = get_rest_client()
parent_dep_labels = rest_client.deployments.get(ctx.deployment.id).get('labels', [])
parent_dep_labels = convert_list_to_dict(parent_dep_labels)
env_type = parent_dep_labels.get('csys-env-type', '')

if env_type != 'Wind-River-Cloud-Platform-Subcloud':
    # get number of subclouds to create
    group_id = 'mock-subcloud{0}'.format(round(time()*1000))
    blueprint_id = ctx.blueprint.id
    number_of_subclouds = len(runtime_properties.get('subcloud_names', []))

    rest_client.deployment_groups.put(
        group_id=group_id,
        blueprint_id=blueprint_id)
    deployment_ids = runtime_properties.get('subcloud_names', [])
    dep_labels = []
    dep_inputs = []
    for _ in range(number_of_subclouds):
        dep_inner_label = {
            'csys-obj-parent': ctx.deployment.id,
            'csys-wrcp-services': 'kubernetes',
            'wrcp-group-name': 'Default',
            'csys-location-lat': '33.5722',
            'csys-location-long': '-112.891',
            'csys-env-type': 'Wind-River-Cloud-Platform-Subcloud',
            'csys-obj-type': 'environment',
            'wrcp-group-id': '1'
        }
        dep_labels.append(convert_dict_to_list(dep_inner_label))
        dep_inputs.append({'file_location': 'resources/subcloud_data.json'})
    # ctx.logger.info('deployment_ids {0}'.format(deployment_ids))
    # ctx.logger.info('dep_labels {0}'.format(dep_labels))
    # ctx.logger.info('dep_inputs {0}'.format(dep_inputs))
    rest_client.deployment_groups.add_deployments(
        group_id,
        new_deployments=[
            {
                'display_name': dep_id,
                'inputs': inp,
                'labels': label
            } for dep_id, inp, label in zip(
                deployment_ids, dep_inputs, dep_labels)]
    )
    attempts = 0
    while True:
        try:
            rest_client.execution_groups.start(group_id, 'install',
                                               concurrency=50)
            break
        except (DeploymentEnvironmentCreationPendingError,
                DeploymentEnvironmentCreationInProgressError) as e:
            attempts += 1
            if attempts > 15:
                raise NonRecoverableError(
                    'Maximum attempts waiting '
                    'for deployment group {group}" {e}.'.format(
                        group=group_id, e=e))
            sleep(5)
            continue
    # subcloud , let's add some more labels
    parent_dep_labels['csys-location-long'] = '-118.4068'
    parent_dep_labels['csys-location-lat'] = '34.1139'
    parent_dep_labels['csys-wrcp-services'] = 'kubernetes'
    parent_dep_labels['csys-location-name'] = 'los angeles ca'
    parent_dep_labels['csys-env-type'] = 'Wind-River-Cloud-Platform-System-Controller'
    labels = convert_dict_to_list(parent_dep_labels)
    rest_client.deployments.update_labels(
        ctx.deployment.id,
        labels=labels)