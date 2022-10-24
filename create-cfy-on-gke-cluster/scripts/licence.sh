#!/bin/bash

set -e

sh -c "cd /tmp && wget ${LICENCE} -O cloudify"
curl -X PUT \
    --header "Tenant: default_tenant" \
    --header "Content-Type: application/json" \
    -u admin:${ADMIN_PASSWORD} \
    --data-binary @/tmp/cloudify
    "${IP}/api/v3.1/license"
ctx logger info "licence installed successfully"
