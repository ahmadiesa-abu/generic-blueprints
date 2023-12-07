#!/bin/bash
ctx logger info "Generate mac address"
mac_address=$(sh -c "tr -dc A-F0-9 < /dev/urandom | head -c 10 | sed -r 's/(..)/\\1:/g;s/:\$//;s/^/02:/'")
ctx instance runtime-properties mac_address "${mac_address}"
deployment_id="$(ctx deployment id)"
LOCATION="/tmp/uploadKey/${deployment_id}"
rm -rf "${LOCATION}"
mkdir -p "${LOCATION}"
ctx instance runtime-properties TEMP_FILE_PATH "${LOCATION}"
ctx logger info "Upload certificates"
ctx download_resource resources/DB.cer "${LOCATION}/DB.cer"
ctx download_resource resources/KEK.cer "${LOCATION}/KEK.cer"
ctx download_resource resources/PK.cer "${LOCATION}/PK.cer"