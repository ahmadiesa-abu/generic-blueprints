#!/usr/bin/env python

import os
import yaml
import shutil
import requests

from requests.auth import HTTPBasicAuth

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


def download_file(url, artifactory_config, headers=None):
    user = artifactory_config.get('artifactory_user')
    password = artifactory_config.get('artifactory_password')
    auth = HTTPBasicAuth(user, password)
    local_filename = url.split('/')[-1]
    fpath = '/tmp/isos/'
    dir_exist = os.path.exists(fpath)
    if not dir_exist:
        os.makedirs(fpath)
    file_path = '{0}{1}'.format(fpath, local_filename)
    verify = artifactory_config.get('artifactory_verify_ssl', True)
    with requests.get(url, headers=headers, auth=auth,
                      verify=verify, stream=True) as r:
        with open(file_path, 'wb+') as f:
            shutil.copyfileobj(r.raw, f)
    return file_path


def _sent_request(request_name: requests, artifactory_config, headers=None,
                  url='', check_status=True, is_json=True):
    user = artifactory_config.get('artifactory_user')
    password = artifactory_config.get('artifactory_password')
    auth = HTTPBasicAuth(user, password)
    verify = artifactory_config.get('artifactory_verify_ssl', True)
    resp = request_name(url=url, headers=headers, auth=auth, verify=verify)
    if check_status:
        resp.raise_for_status()
    return resp.json() if is_json else resp


def get_latest_version(artifactory_config):
    manifest_source = artifactory_config.get('manifest_source')
    artifactory_url = artifactory_config.get('artifactory_url')
    url = '{0}/artifactory/api/storage/isgedge-generic-local-mw/artifacts/' \
          'hzp/manifests/ece/{1}/?lastModified'.format(
              artifactory_url, manifest_source)
    resp = _sent_request(request_name=requests.get,
                         artifactory_config=artifactory_config,
                         url=url
                         )
    url_file = resp.get('uri')
    resp = _sent_request(request_name=requests.get,
                         artifactory_config=artifactory_config,
                         url=url_file
                         )
    download_uri = resp.get('downloadUri')
    fp = download_file(url=download_uri, artifactory_config=artifactory_config)
    with open(fp, 'r') as f:
        data_loaded = yaml.safe_load(f)
    try:
        return data_loaded.get("global", {}).get(
            'components', [])[0].get('version')
    except (KeyError, IndexError):
        return None


def construct_artifactory_url(artifactory_config, production=False):
    manifest_version = artifactory_config.get('software_version')
    artifactory_url = artifactory_config.get('artifactory_url')
    manifest_source = artifactory_config.get('manifest_source')
    if not manifest_version:
        manifest_version = get_latest_version(artifactory_config)
    manifest_version = manifest_version.replace("/", "")
    if production:
        manufacture_os_filename = "Ubuntu-22.04.x86_64-prod-{}.iso".format(
            manifest_version)
        download_url = "{0}/artifactory/isgedge-generic-virtual" \
                       "/hzp/ece/manufacturing-os/prod/{1}/{2}/{3}".\
            format(artifactory_url, manifest_source, manifest_version,
                   manufacture_os_filename)
    else:
        manufacture_os_filename = "Ubuntu-22.04.x86_64-staging-{}.iso".format(
            manifest_version)
        download_url = "{0}/artifactory/isgedge-generic-virtual" \
                       "/hzp/ece/manufacturing-os/{1}/{2}/{3}".format(
                           artifactory_url, manifest_source,
                           manifest_version, manufacture_os_filename)
    return download_url, manufacture_os_filename


if __name__ == '__main__':
    artifactory_config = inputs.get('artifactory_config')
    prod_ver = inputs.get('production_version')
    download_url, manufacture_os_filename = \
        construct_artifactory_url(artifactory_config=artifactory_config,
                                  production=prod_ver)
    target_path = '/tmp/isos/{0}'.format(manufacture_os_filename)
    ctx.logger.info('The iso: {0} will be download. From: {1}. To: {2}'.
                    format(manufacture_os_filename, download_url, target_path))
    ctx.instance.runtime_properties['iso_path'] = target_path
    ctx.instance.runtime_properties['iso_filename'] = manufacture_os_filename
    download_file(download_url, artifactory_config)
    ctx.logger.info('ISO downloaded.')
    