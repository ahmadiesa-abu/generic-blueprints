output "db_instance_address" {
  description = "The connection address"
  value       = aws_db_instance.db.address
}

output "db_instance_port" {
  description = "The connection port"
  value       = aws_db_instance.db.port
}

output "db_instance_name" {
  description = "The database name"
  value       = aws_db_instance.db.db_name
}

output "db_instance_username" {
  description = "The master username for the database"
  value       = aws_db_instance.db.username
  sensitive   = true
}

output "db_instance_password" {
  description = "The database password (this password may be old, because Terraform doesn't track it after initial creation)"
  value       = aws_db_instance.db.password
  sensitive   = true
}
