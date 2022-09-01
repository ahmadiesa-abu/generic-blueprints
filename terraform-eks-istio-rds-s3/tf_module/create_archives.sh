rm -rf *.zip || true
zip -r -X eks.zip eks
zip -r -X istio.zip istio
zip -r -X rds.zip rds
zip -r -X s3.zip s3
zip -r -X service_account.zip service_account
zip -r -X vpc.zip vpc
