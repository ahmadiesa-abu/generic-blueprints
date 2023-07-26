#!/bin/bash
set -e

if [[  "${BOOL_VAR}" == "true" ]]
then
    ctx logger info "Got true value"
else
    ctx logger info "Got false value"
fi