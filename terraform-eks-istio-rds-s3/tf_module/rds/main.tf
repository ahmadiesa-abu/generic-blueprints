resource "aws_db_instance" "db" {
    engine = var.db_engine
    engine_version = var.db_engine_version
    instance_class = var.instance_type
    db_name = var.db_name
    identifier = var.db_identifier
    username = var.db_username
    password = var.db_password
    db_subnet_group_name = var.database_subnet_group_name
    vpc_security_group_ids = [var.security_group_id]
    publicly_accessible = true
    skip_final_snapshot = true
    allocated_storage = 50
    max_allocated_storage = 1000
}
