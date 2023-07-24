#!/bin/bash
set -e

# Set deployment directory
export DEPLOYMENT_DIR=""
DEPLOYMENT_DIR="/opt/manager/resources/deployments/$(ctx tenant_name)/$(ctx deployment id)"
if [[ -z "${DEPLOYMENT_DIR}" ]]
then
    ctx logger info "Unable to determine deployment directory"
    exit 1
fi

ctx instance runtime-properties deployment_directory "$DEPLOYMENT_DIR"
ctx logger info "Set deployment directory to $DEPLOYMENT_DIR"

# Change to deployment directory and download EO charts
pushd "$DEPLOYMENT_DIR" || return 1
mkdir test-folder
touch test-folder/.test
touch test-folder/test
zip -r test-folder.zip test-folder/

popd || return 1