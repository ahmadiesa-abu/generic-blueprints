# Specify the provider and access details
provider "null" {
}

variable "message" {
  type = string
}

variable "message2" {
  type = string
}


resource "null_resource" "foo2" {

provisioner "local-exec" {
  command = "echo '${var.message}' > /tmp/sometest.txt && echo '${var.message2}' >> /tmp/sometest.txt"
}

}

output "out2" {
  value = "done with my test :)"
  sensitive = false
}
