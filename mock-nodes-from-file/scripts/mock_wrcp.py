import json

from time import sleep
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
dep_labels = rest_client.deployments.get(ctx.deployment.id).get('labels', [])
ctx.logger.info('labels {0}'.format(dep_labels))
dep_labels = convert_list_to_dict(dep_labels)
is_subcloud = dep_labels.get('is_subcloud', '')

if is_subcloud != 'True':
    # get number of subclouds to create
    group_id = 'mock-subcloud'
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
            'is_subcloud': 'True',
            'csys-obj-parent': ctx.deployment.id
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
