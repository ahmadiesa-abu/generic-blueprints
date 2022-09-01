# Ports needed to correctly install Istio for the error message: transport: Error while dialing dial tcp xx.xx.xx.xx15012: i/o timeout
locals {
  istio_ports = [
    {
      description = "Envoy admin port / outbound"
      from_port   = 15000
      to_port     = 15001
    },
    {
      description = "Debug port"
      from_port   = 15004
      to_port     = 15004
    },
    {
      description = "Envoy inbound"
      from_port   = 15006
      to_port     = 15006
    },
    {
      description = "HBONE mTLS tunnel port / secure networks XDS and CA services (Plaintext)"
      from_port   = 15008
      to_port     = 15010
    },
    {
      description = "XDS and CA services (TLS and mTLS)"
      from_port   = 15012
      to_port     = 15012
    },
    {
      description = "Control plane monitoring"
      from_port   = 15014
      to_port     = 15014
    },
    {
      description = "Webhook container port, forwarded from 443"
      from_port   = 15017
      to_port     = 15017
    },
    {
      description = "Merged Prometheus telemetry from Istio agent, Envoy, and application, Health checks"
      from_port   = 15020
      to_port     = 15021
    },
    {
      description = "DNS port"
      from_port   = 15053
      to_port     = 15053
    },
    {
      description = "Envoy Prometheus telemetry"
      from_port   = 15090
      to_port     = 15090
    },
    {
      description = "aws-load-balancer-controller"
      from_port   = 9443
      to_port     = 9443
    }
  ]

  ingress_rules = {
    for ikey, ivalue in local.istio_ports :
    "${ikey}_ingress" => {
      description = ivalue.description
      protocol    = "tcp"
      from_port   = ivalue.from_port
      to_port     = ivalue.to_port
      type        = "ingress"
      self        = true
    }
  }

  egress_rules = {
    for ekey, evalue in local.istio_ports :
    "${ekey}_egress" => {
      description = evalue.description
      protocol    = "tcp"
      from_port   = evalue.from_port
      to_port     = evalue.to_port
      type        = "egress"
      self        = true
    }
  }
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  create_cloudwatch_log_group     = false

  cluster_addons = {
    coredns = {
      resolve_conflicts = "OVERWRITE"
    }
    kube-proxy = {}
    vpc-cni = {
      resolve_conflicts = "OVERWRITE"
    }
  }

  eks_managed_node_group_defaults = {
    ami_type       = "AL2_x86_64"
    disk_size      = 20
    instance_types = [var.instance_type]
  }

  eks_managed_node_groups = {
    group = {
      name         = var.node_group_name
      min_size     = var.minimum_nodes
      max_size     = var.maximum_nodes
      desired_size = var.desired_nodes

      capacity_type = "ON_DEMAND"
    }
  }


  # IMPORTANT
  node_security_group_additional_rules = merge(
    local.ingress_rules,
    local.egress_rules
  )

}

# Port needed to solve the error
# Internal error occurred: failed calling
# webhook "namespace.sidecar-injector.istio.io": failed to
# call webhook: Post "https://istiod.istio-system.svc:443/inject?timeout=10s": # context deadline exceeded
resource "aws_security_group_rule" "allow_sidecar_injection" {
  description = "Webhook container port, From Control Plane"
  protocol    = "tcp"
  type        = "ingress"
  from_port   = 15017
  to_port     = 15017

  security_group_id        = module.eks.node_security_group_id
  source_security_group_id = module.eks.cluster_primary_security_group_id
}
