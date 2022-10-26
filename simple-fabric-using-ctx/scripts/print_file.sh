#!/bin/bash

echo "printing ${1}"
cat ${1}

echo "printing a secret"
echo $(ctx node properties some_secret)

ctx instance runtime_properties test "100"