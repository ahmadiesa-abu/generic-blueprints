from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
import yaml

BLUEPRINT_TEMPLATE = """
tosca_definitions_version: cloudify_dsl_1_4

imports:
  - cloudify/types/types.yaml
  - plugin:cloudify-vsphere-plugin

description: >
  Devices blueprint to add various devices to vSphere VM

inputs:
  vsphere_secret:
    default: ""
    type: string

  vm_name:
    default: ""
    type: string

dsl_definitions:
  connection_config: &connection_config
    username: { get_secret: [ vsphere_secret, username ] }
    password: { get_secret: [ vsphere_secret, password ] }
    host: { get_secret: [ vsphere_secret, host ] }
    port: { get_secret: [ vsphere_secret, port ] }
    datacenter_name: { get_secret: [ vsphere_secret, datacenter_name ] }
    resource_pool_name: { get_secret: [ vsphere_secret, resource_pool_name ] }
    auto_placement: { get_secret: [ vsphere_secret, auto_placement ] }
    allow_insecure: { get_secret: [ vsphere_secret, allow_insecure ] }

node_templates:
  vm:
    type: cloudify.nodes.vsphere.Server
    properties:
      wait_ip: true
      use_external_resource: true
      connection_config: *connection_config
      agent_config:
        install_method: none
      server:
        name: { get_input: vm_name }
"""

blueprint = yaml.safe_load(BLUEPRINT_TEMPLATE)
devices_list = inputs.get('devices_list', [])

if devices_list:
    previously_added = []
    for device in devices_list:
        device_type = device.get('type', '')
        if device_type in ['usb', 'serial', 'pci']:
            node_name = f"{device_type}_device"
            node_type = f"cloudify.nodes.vsphere.{device_type.upper()}Device" if device_type != 'serial' \
                else  f"cloudify.nodes.vsphere.{device_type.capitalize()}Port"
            relationship = f"cloudify.relationships.vsphere.{device_type}_connected_to_server"

            node_template = {
                node_name: {
                    'type': node_type,
                    'properties': {
                        'connection_config': '*connection_config',
                        'device_name': '{0}'.format(device.get('device_name', ''))
                    },
                    'relationships': [{
                            'target': 'vm',
                            'type': relationship
                        }
                    ]
                }
            }
            if device_type != 'usb':
                node_template[node_name]['properties']['turn_off_vm'] = True
            if previously_added:
                node_template[node_name]['relationships'].append({
                    'target': previously_added[-1],
                    'type': 'cloudify.relationships.depends_on'
                })
            blueprint['node_templates'].update(node_template)
            previously_added.append(node_name)

full_yaml = yaml.dump(blueprint, default_flow_style=False)

anchor_yaml = full_yaml.replace("'*connection_config'", '*id001')


with open('/tmp/blueprint.yaml', 'w') as f:
    f.write(anchor_yaml)
