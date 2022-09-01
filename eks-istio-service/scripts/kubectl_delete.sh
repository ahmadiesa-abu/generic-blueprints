#!/bin/bash -e

resource_path=$(ctx download-resource ${gateway_resource_path})
ctx logger info "Resource downloaded into ${resource_path}"

namespace=${istio_ingress_namespace}

sed -i "s/MICROSERVICE_NAMESPACE/${istio_ingress_namespace}/g" ${resource_path}
sed -i "s/MICROSERVICE_NAME/${MICROSERVICE_NAME}/g" ${resource_path}
sed -i "s/MICROSERVICE_PORT/${MICROSERVICE_PORT}/g" ${resource_path}

./tmp/kubectl/kubectl config set-cluster cfc --server=${host} --insecure-skip-tls-verify=true
./tmp/kubectl/kubectl config set-context cfc --cluster=cfc
./tmp/kubectl/kubectl config set-credentials user --token=${token}
./tmp/kubectl/kubectl config set-context cfc --user=user
./tmp/kubectl/kubectl config use-context cfc

./tmp/kubectl/kubectl delete -f ${resource_path} -n ${namespace}

rm -rf ${resource_path}
