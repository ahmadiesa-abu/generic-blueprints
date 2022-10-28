#!/bin/bash

echo "printing ${1}"
cat ${1}

TARGET_DIR="${1}"

echo "printing a secret"
x="$(ctx node properties some_secret)"
     
echo $(ctx node properties some_secret)

echo ${TARGET_DIR}

ctx instance runtime_properties test "100"