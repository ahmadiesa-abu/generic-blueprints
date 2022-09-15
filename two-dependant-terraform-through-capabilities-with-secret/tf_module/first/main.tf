# Specify the provider and access details
provider "null" {
}

resource "null_resource" "foo1" {
    triggers = {
        cluster_instance_ids = "dummy_id"
    }
    depends_on = [ null_resource.foo2 ]
    count = 2
}

resource "null_resource" "foo2" {
}

output "out" {
  value = "what the hell?"
  sensitive = false
}
