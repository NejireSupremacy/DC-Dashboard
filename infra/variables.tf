variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
}

variable "project_name" {
  description = "Base project name used in resource naming."
  type        = string
}

variable "environment" {
  description = "Environment name used in resource naming and tags."
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets. Use at least two."
  type        = list(string)
}

variable "container_port" {
  description = "Port exposed by the container."
  type        = number
  default     = 8501
}

variable "health_check_path" {
  description = "HTTP path used by the ALB health check."
  type        = string
  default     = "/"
}

variable "task_cpu" {
  description = "Fargate task CPU units."
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Fargate task memory in MiB."
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Desired number of ECS tasks."
  type        = number
  default     = 1
}

variable "image_tag" {
  description = "Docker image tag to deploy from ECR."
  type        = string
  default     = "latest"
}
