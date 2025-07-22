import streamlit as st
import requests
import base64
import io
import zipfile
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Terraform Code Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem 0;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.stButton > button {
    border-radius: 20px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: bold;
    transition: all 0.3s;
}
.stExpander {
    border: 1px solid #ddd;
    border-radius: 10px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Data Classes
@dataclass
class TerraformPattern:
    name: str
    description: str
    path: str
    download_url: str
    category: str
    provider: str
    complexity: str
    files: List[str] = None

# GitHub Pattern Fetcher Class
class GitHubPatternFetcher:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}" if token else None
        }
    
    @st.cache_data(ttl=3600)
    def fetch_aws_patterns(_self) -> List[TerraformPattern]:
        """Fetch AWS Terraform patterns from popular repositories"""
        patterns = []
        
        # Replace the predefined_patterns section in your GitHubPatternFetcher class with this expanded list

        predefined_patterns = [
            # Networking (Most Essential)
            {
                "name": "VPC Module",
                "description": "Complete VPC setup with public/private subnets, NAT gateway, and internet gateway",
                "category": "networking",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Security Groups",
                "description": "Reusable security groups for web, database, and application tiers",
                "category": "security",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "NAT Gateway",
                "description": "NAT Gateway with Elastic IP for private subnet internet access",
                "category": "networking",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Compute (Essential)
            {
                "name": "EC2 Instance",
                "description": "Configurable EC2 instance with security groups and key pair management",
                "category": "compute",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Auto Scaling Group",
                "description": "Auto Scaling Group with Launch Template and multiple AZ support",
                "category": "compute",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Lambda Function",
                "description": "Serverless Lambda function with IAM role, CloudWatch logs, and API Gateway integration",
                "category": "compute",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "EKS Cluster",
                "description": "Complete EKS cluster with node groups, IRSA, and add-ons",
                "category": "compute",
                "complexity": "advanced",
                "files": ["main.tf", "variables.tf", "outputs.tf", "eks-cluster.tf", "eks-nodes.tf"]
            },
            {
                "name": "ECS Cluster",
                "description": "ECS cluster with Fargate support and service discovery",
                "category": "compute",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Storage (Essential)
            {
                "name": "S3 Bucket",
                "description": "S3 bucket with versioning, encryption, lifecycle policies, and CloudFront integration",
                "category": "storage",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "EFS File System",
                "description": "Elastic File System with mount targets and backup policies",
                "category": "storage",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Database (Essential)
            {
                "name": "RDS Database",
                "description": "MySQL/PostgreSQL RDS with Multi-AZ, read replicas, and automated backups",
                "category": "database",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "ElastiCache Redis",
                "description": "Redis cluster with replication group and subnet group",
                "category": "database",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "DynamoDB Table",
                "description": "DynamoDB table with GSI, backup, and point-in-time recovery",
                "category": "database",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Load Balancing (Essential)
            {
                "name": "Application Load Balancer",
                "description": "ALB with target groups, health checks, SSL termination, and WAF integration",
                "category": "networking",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Network Load Balancer",
                "description": "NLB for high-performance TCP/UDP load balancing",
                "category": "networking",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Content Delivery & DNS
            {
                "name": "CloudFront Distribution",
                "description": "CloudFront CDN with S3 origin, custom headers, and caching policies",
                "category": "networking",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Route53 DNS",
                "description": "Route53 hosted zone with health checks and alias records",
                "category": "networking",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # API & Messaging (High Usage)
            {
                "name": "API Gateway",
                "description": "REST API Gateway with Lambda integration, CORS, and API keys",
                "category": "compute",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "SQS Queue",
                "description": "SQS queue with dead letter queue and visibility timeout",
                "category": "messaging",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "SNS Topic",
                "description": "SNS topic with subscriptions and delivery policies",
                "category": "messaging",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Security & Secrets (Essential)
            {
                "name": "IAM Roles & Policies",
                "description": "Reusable IAM roles for EC2, Lambda, and EKS with least privilege policies",
                "category": "security",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Secrets Manager",
                "description": "AWS Secrets Manager for database credentials and API keys with rotation",
                "category": "security",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "Parameter Store",
                "description": "Systems Manager Parameter Store for configuration management",
                "category": "security",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # Monitoring & Logging (Essential)
            {
                "name": "CloudWatch Monitoring",
                "description": "CloudWatch alarms, dashboards, and log groups with metric filters",
                "category": "monitoring",
                "complexity": "intermediate",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            
            # CI/CD & DevOps
            {
                "name": "ECR Repository",
                "description": "Elastic Container Registry with lifecycle policies and image scanning",
                "category": "devops",
                "complexity": "beginner",
                "files": ["main.tf", "variables.tf", "outputs.tf"]
            },
            {
                "name": "CodePipeline",
                "description": "Complete CI/CD pipeline with CodeBuild, CodeDeploy, and S3 artifacts",
                "category": "devops",
                "complexity": "advanced",
                "files": ["main.tf", "variables.tf", "outputs.tf", "buildspec.yml"]
            },
            
            # Complete Solutions (Popular Architectures)
            {
                "name": "3-Tier Web Application",
                "description": "Complete 3-tier architecture with ALB, ASG, RDS, and CloudFront",
                "category": "architecture",
                "complexity": "advanced",
                "files": ["main.tf", "variables.tf", "outputs.tf", "web-tier.tf", "app-tier.tf", "db-tier.tf"]
            },
            {
                "name": "Serverless Web App",
                "description": "Serverless architecture with Lambda, API Gateway, DynamoDB, and S3",
                "category": "architecture",
                "complexity": "advanced",
                "files": ["main.tf", "variables.tf", "outputs.tf", "lambda.tf", "api-gateway.tf"]
            },
            {
                "name": "Data Lake Architecture",
                "description": "S3 data lake with Glue, Athena, and EMR for big data processing",
                "category": "architecture",
                "complexity": "advanced",
                "files": ["main.tf", "variables.tf", "outputs.tf", "data-lake.tf", "glue.tf"]
            }
        ]        
        for pattern_data in predefined_patterns:
            pattern = TerraformPattern(
                name=pattern_data["name"],
                description=pattern_data["description"],
                path=f"terraform-aws-modules/{pattern_data['name'].lower().replace(' ', '-')}",
                download_url="https://github.com/terraform-aws-modules",
                category=pattern_data["category"],
                provider="aws",
                complexity=pattern_data["complexity"],
                files=pattern_data["files"]
            )
            patterns.append(pattern)
        
        return patterns
    # Add these additional methods to your GitHubPatternFetcher class
    def _get_dynamodb_code(self) -> Dict[str, str]:
    return {
            "main.tf": '''# DynamoDB Table
            resource "aws_dynamodb_table" "main" {
            name         = "${var.environment}-${var.table_name}"
            billing_mode = var.billing_mode
            hash_key     = var.hash_key
            range_key    = var.range_key

            read_capacity  = var.billing_mode == "PROVISIONED" ? var.read_capacity : null
            write_capacity = var.billing_mode == "PROVISIONED" ? var.write_capacity : null

            attribute {
                name = var.hash_key
                type = var.hash_key_type
            }

            dynamic "attribute" {
                for_each = var.range_key != null ? [1] : []
                content {
                name = var.range_key
                type = var.range_key_type
                }
            }

            dynamic "attribute" {
                for_each = var.global_secondary_indexes
                content {
                name = attribute.value.hash_key
                type = attribute.value.hash_key_type
                }
            }

            # Global Secondary Indexes
            dynamic "global_secondary_index" {
                for_each = var.global_secondary_indexes
                content {
                name     = global_secondary_index.value.name
                hash_key = global_secondary_index.value.hash_key
                range_key = global_secondary_index.value.range_key

                write_capacity = var.billing_mode == "PROVISIONED" ? global_secondary_index.value.write_capacity : null
                read_capacity  = var.billing_mode == "PROVISIONED" ? global_secondary_index.value.read_capacity : null

                projection_type    = global_secondary_index.value.projection_type
                non_key_attributes = global_secondary_index.value.non_key_attributes
                }
            }

            # Local Secondary Indexes
            dynamic "local_secondary_index" {
                for_each = var.local_secondary_indexes
                content {
                name               = local_secondary_index.value.name
                range_key          = local_secondary_index.value.range_key
                projection_type    = local_secondary_index.value.projection_type
                non_key_attributes = local_secondary_index.value.non_key_attributes
                }
            }

            # TTL
            dynamic "ttl" {
                for_each = var.ttl_attribute_name != null ? [1] : []
                content {
                attribute_name = var.ttl_attribute_name
                enabled        = var.ttl_enabled
                }
            }

            # Encryption
            server_side_encryption {
                enabled     = var.encryption_enabled
                kms_key_arn = var.kms_key_arn
            }

            # Point in time recovery
            point_in_time_recovery {
                enabled = var.point_in_time_recovery
            }

            # Stream
            stream_enabled   = var.stream_enabled
            stream_view_type = var.stream_enabled ? var.stream_view_type : null

            tags = merge(var.common_tags, {
                Name = "${var.environment}-${var.table_name}"
            })
            }

            # Auto Scaling for DynamoDB
            resource "aws_appautoscaling_target" "read" {
            count              = var.billing_mode == "PROVISIONED" && var.autoscaling_enabled ? 1 : 0
            max_capacity       = var.autoscaling_read_max_capacity
            min_capacity       = var.autoscaling_read_min_capacity
            resource_id        = "table/${aws_dynamodb_table.main.name}"
            scalable_dimension = "dynamodb:table:ReadCapacityUnits"
            service_namespace  = "dynamodb"
            }

            resource "aws_appautoscaling_policy" "read" {
            count              = var.billing_mode == "PROVISIONED" && var.autoscaling_enabled ? 1 : 0
            name               = "${var.environment}-${var.table_name}-read-scaling-policy"
            policy_type        = "TargetTrackingScaling"
            resource_id        = aws_appautoscaling_target.read[0].resource_id
            scalable_dimension = aws_appautoscaling_target.read[0].scalable_dimension
            service_namespace  = aws_appautoscaling_target.read[0].service_namespace

            target_tracking_scaling_policy_configuration {
                predefined_metric_specification {
                predefined_metric_type = "DynamoDBReadCapacityUtilization"
                }
                target_value = var.autoscaling_read_target_value
            }
            }

            resource "aws_appautoscaling_target" "write" {
            count              = var.billing_mode == "PROVISIONED" && var.autoscaling_enabled ? 1 : 0
            max_capacity       = var.autoscaling_write_max_capacity
            min_capacity       = var.autoscaling_write_min_capacity
            resource_id        = "table/${aws_dynamodb_table.main.name}"
            scalable_dimension = "dynamodb:table:WriteCapacityUnits"
            service_namespace  = "dynamodb"
            }

            resource "aws_appautoscaling_policy" "write" {
            count              = var.billing_mode == "PROVISIONED" && var.autoscaling_enabled ? 1 : 0
            name               = "${var.environment}-${var.table_name}-write-scaling-policy"
            policy_type        = "TargetTrackingScaling"
            resource_id        = aws_appautoscaling_target.write[0].resource_id
            scalable_dimension = aws_appautoscaling_target.write[0].scalable_dimension
            service_namespace  = aws_appautoscaling_target.write[0].service_namespace

            target_tracking_scaling_policy_configuration {
                predefined_metric_specification {
                predefined_metric_type = "DynamoDBWriteCapacityUtilization"
                }
                target_value = var.autoscaling_write_target_value
            }
            }''',
                    "variables.tf": '''variable "environment" {
            description = "Environment name"
            type        = string
            default     = "dev"
            }

            variable "table_name" {
            description = "Name of the DynamoDB table"
            type        = string
            }

            variable "billing_mode" {
            description = "Billing mode for the table"
            type        = string
            default     = "PAY_PER_REQUEST"
            validation {
                condition     = contains(["PROVISIONED", "PAY_PER_REQUEST"], var.billing_mode)
                error_message = "Billing mode must be PROVISIONED or PAY_PER_REQUEST."
            }
            }

            variable "hash_key" {
            description = "Hash key (partition key) for the table"
            type        = string
            }

            variable "hash_key_type" {
            description = "Hash key attribute type"
            type        = string
            default     = "S"
            }

            variable "range_key" {
            description = "Range key (sort key) for the table"
            type        = string
            default     = null
            }

            variable "range_key_type" {
            description = "Range key attribute type"
            type        = string
            default     = "S"
            }

            variable "read_capacity" {
            description = "Read capacity units"
            type        = number
            default     = 5
            }

            variable "write_capacity" {
            description = "Write capacity units"
            type        = number
            default     = 5
            }

            variable "global_secondary_indexes" {
            description = "Global secondary indexes"
            type = list(object({
                name               = string
                hash_key           = string
                hash_key_type      = string
                range_key          = string
                projection_type    = string
                non_key_attributes = list(string)
                read_capacity      = number
                write_capacity     = number
            }))
            default = []
            }

            variable "local_secondary_indexes" {
            description = "Local secondary indexes"
            type = list(object({
                name               = string
                range_key          = string
                projection_type    = string
                non_key_attributes = list(string)
            }))
            default = []
            }

            variable "ttl_attribute_name" {
            description = "TTL attribute name"
            type        = string
            default     = null
            }

            variable "ttl_enabled" {
            description = "Enable TTL"
            type        = bool
            default     = true
            }

            variable "encryption_enabled" {
            description = "Enable server-side encryption"
            type        = bool
            default     = true
            }

            variable "kms_key_arn" {
            description = "KMS key ARN for encryption"
            type        = string
            default     = null
            }

            variable "point_in_time_recovery" {
            description = "Enable point in time recovery"
            type        = bool
            default     = true
            }

            variable "stream_enabled" {
            description = "Enable DynamoDB streams"
            type        = bool
            default     = false
            }

            variable "stream_view_type" {
            description = "Stream view type"
            type        = string
            default     = "NEW_AND_OLD_IMAGES"
            }

            variable "autoscaling_enabled" {
            description = "Enable auto scaling"
            type        = bool
            default     = false
            }

            variable "autoscaling_read_min_capacity" {
            description = "Auto scaling read min capacity"
            type        = number
            default     = 5
            }

            variable "autoscaling_read_max_capacity" {
            description = "Auto scaling read max capacity"
            type        = number
            default     = 100
            }

            variable "autoscaling_read_target_value" {
            description = "Auto scaling read target value"
            type        = number
            default     = 70
            }

            variable "autoscaling_write_min_capacity" {
            description = "Auto scaling write min capacity"
            type        = number
            default     = 5
            }

            variable "autoscaling_write_max_capacity" {
            description = "Auto scaling write max capacity"
            type        = number
            default     = 100
            }

            variable "autoscaling_write_target_value" {
            description = "Auto scaling write target value"
            type        = number
            default     = 70
            }

            variable "common_tags" {
            description = "Common tags for all resources"
            type        = map(string)
            default = {
                Terraform   = "true"
                Environment = "dev"
            }
            }''',
                    "outputs.tf": '''output "table_name" {
            description = "DynamoDB table name"
            value       = aws_dynamodb_table.main.name
            }

            output "table_id" {
            description = "DynamoDB table ID"
            value       = aws_dynamodb_table.main.id
            }

            output "table_arn" {
            description = "DynamoDB table ARN"
            value       = aws_dynamodb_table.main.arn
            }

            output "table_stream_arn" {
            description = "DynamoDB table stream ARN"
            value       = aws_dynamodb_table.main.stream_arn
            }

            output "table_stream_label" {
            description = "DynamoDB table stream label"
            value       = aws_dynamodb_table.main.stream_label
            }'''
                }

            def _get_security_groups_code(self) -> Dict[str, str]:
                return {
                    "main.tf": '''# Web Tier Security Group
            resource "aws_security_group" "web" {
            name_prefix = "${var.environment}-web-"
            vpc_id      = var.vpc_id
            description = "Security group for web tier"

            # HTTP access
            ingress {
                from_port   = 80
                to_port     = 80
                protocol    = "tcp"
                cidr_blocks = ["0.0.0.0/0"]
                description = "HTTP"
            }

            # HTTPS access
            ingress {
                from_port   = 443
                to_port     = 443
                protocol    = "tcp"
                cidr_blocks = ["0.0.0.0/0"]
                description = "HTTPS"
            }

            # SSH access (restricted)
            ingress {
                from_port   = 22
                to_port     = 22
                protocol    = "tcp"
                cidr_blocks = var.ssh_allowed_cidrs
                description = "SSH"
            }

            egress {
                from_port   = 0
                to_port     = 0
                protocol    = "-1"
                cidr_blocks = ["0.0.0.0/0"]
                description = "All outbound traffic"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-web-sg"
                Tier = "Web"
            })
            }

            # Application Tier Security Group
            resource "aws_security_group" "app" {
            name_prefix = "${var.environment}-app-"
            vpc_id      = var.vpc_id
            description = "Security group for application tier"

            # Allow traffic from web tier
            ingress {
                from_port       = var.app_port
                to_port         = var.app_port
                protocol        = "tcp"
                security_groups = [aws_security_group.web.id]
                description     = "Application port from web tier"
            }

            # SSH access (restricted)
            ingress {
                from_port   = 22
                to_port     = 22
                protocol    = "tcp"
                cidr_blocks = var.ssh_allowed_cidrs
                description = "SSH"
            }

            egress {
                from_port   = 0
                to_port     = 0
                protocol    = "-1"
                cidr_blocks = ["0.0.0.0/0"]
                description = "All outbound traffic"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-app-sg"
                Tier = "Application"
            })
            }

            # Database Tier Security Group
            resource "aws_security_group" "db" {
            name_prefix = "${var.environment}-db-"
            vpc_id      = var.vpc_id
            description = "Security group for database tier"

            # MySQL/Aurora access from app tier
            ingress {
                from_port       = 3306
                to_port         = 3306
                protocol        = "tcp"
                security_groups = [aws_security_group.app.id]
                description     = "MySQL from application tier"
            }

            # PostgreSQL access from app tier
            ingress {
                from_port       = 5432
                to_port         = 5432
                protocol        = "tcp"
                security_groups = [aws_security_group.app.id]
                description     = "PostgreSQL from application tier"
            }

            # Redis access from app tier
            ingress {
                from_port       = 6379
                to_port         = 6379
                protocol        = "tcp"
                security_groups = [aws_security_group.app.id]
                description     = "Redis from application tier"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-db-sg"
                Tier = "Database"
            })
            }

            # ALB Security Group
            resource "aws_security_group" "alb" {
            name_prefix = "${var.environment}-alb-"
            vpc_id      = var.vpc_id
            description = "Security group for Application Load Balancer"

            # HTTP access
            ingress {
                from_port   = 80
                to_port     = 80
                protocol    = "tcp"
                cidr_blocks = ["0.0.0.0/0"]
                description = "HTTP"
            }

            # HTTPS access
            ingress {
                from_port   = 443
                to_port     = 443
                protocol    = "tcp"
                cidr_blocks = ["0.0.0.0/0"]
                description = "HTTPS"
            }

            egress {
                from_port   = 0
                to_port     = 0
                protocol    = "-1"
                cidr_blocks = ["0.0.0.0/0"]
                description = "All outbound traffic"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-alb-sg"
                Tier = "Load Balancer"
            })
            }

            # EKS Node Group Security Group
            resource "aws_security_group" "eks_nodes" {
            count       = var.create_eks_sg ? 1 : 0
            name_prefix = "${var.environment}-eks-nodes-"
            vpc_id      = var.vpc_id
            description = "Security group for EKS worker nodes"

            # Allow nodes to communicate with each other
            ingress {
                from_port = 0
                to_port   = 0
                protocol  = "-1"
                self      = true
                description = "Node to node communication"
            }

            # Allow pods to communicate with the cluster API Server
            ingress {
                from_port   = 1025
                to_port     = 65535
                protocol    = "tcp"
                cidr_blocks = var.cluster_endpoint_private_access_cidrs
                description = "API server to nodes"
            }

            egress {
                from_port   = 0
                to_port     = 0
                protocol    = "-1"
                cidr_blocks = ["0.0.0.0/0"]
                description = "All outbound traffic"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-eks-nodes-sg"
                Tier = "EKS Nodes"
            })
            }

            # Lambda Security Group
            resource "aws_security_group" "lambda" {
            count       = var.create_lambda_sg ? 1 : 0
            name_prefix = "${var.environment}-lambda-"
            vpc_id      = var.vpc_id
            description = "Security group for Lambda functions"

            egress {
                from_port   = 0
                to_port     = 0
                protocol    = "-1"
                cidr_blocks = ["0.0.0.0/0"]
                description = "All outbound traffic"
            }

            tags = merge(var.common_tags, {
                Name = "${var.environment}-lambda-sg"
                Tier = "Lambda"
            })
            }''',
                    "variables.tf": '''variable "environment" {
            description = "Environment name"
            type        = string
            default     = "dev"
            }

            variable "vpc_id" {
            description = "VPC ID where security groups will be created"
            type        = string
            }

            variable "ssh_allowed_cidrs" {
            description = "CIDR blocks allowed for SSH access"
            type        = list(string)
            default     = ["10.0.0.0/8"]
            }

            variable "app_port" {
            description = "Application port number"
            type        = number
            default     = 8080
            }

            variable "create_eks_sg" {
            description = "Create EKS security group"
            type        = bool
            default     = false
            }

            variable "create_lambda_sg" {
            description = "Create Lambda security group"
            type        = bool
            default     = false
            }

            variable "cluster_endpoint_private_access_cidrs" {
            description = "CIDR blocks for EKS cluster endpoint private access"
            type        = list(string)
            default     = ["10.0.0.0/8"]
            }

            variable "common_tags" {
            description = "Common tags for all resources"
            type        = map(string)
            default = {
                Terraform   = "true"
                Environment = "dev"
            }
            }''',
                    "outputs.tf": '''output "web_security_group_id" {
            description = "Web tier security group ID"
            value       = aws_security_group.web.id
            }

            output "app_security_group_id" {
            description = "Application tier security group ID"
            value       = aws_security_group.app.id
            }

            output "db_security_group_id" {
            description = "Database tier security group ID"
            value       = aws_security_group.db.id
            }

            output "alb_security_group_id" {
            description = "ALB security group ID"
            value       = aws_security_group.alb.id
            }

            output "eks_nodes_security_group_id" {
            description = "EKS nodes security group ID"
            value       = var.create_eks_sg ? aws_security_group.eks_nodes[0].id : null
            }

            output "lambda_security_group_id" {
            description = "Lambda security group ID"
            value       = var.create_lambda_sg ? aws_security_group.lambda[0].id : null
            }'''
                }
    
    
    def _get_api_gateway_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# API Gateway REST API
    resource "aws_api_gateway_rest_api" "main" {
    name        = "${var.environment}-${var.api_name}"
    description = var.api_description

    endpoint_configuration {
        types = [var.endpoint_type]
    }

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.api_name}"
    })
    }

    # API Gateway Resource
    resource "aws_api_gateway_resource" "proxy" {
    rest_api_id = aws_api_gateway_rest_api.main.id
    parent_id   = aws_api_gateway_rest_api.main.root_resource_id
    path_part   = "{proxy+}"
    }

    # API Gateway Method
    resource "aws_api_gateway_method" "proxy" {
    rest_api_id   = aws_api_gateway_rest_api.main.id
    resource_id   = aws_api_gateway_resource.proxy.id
    http_method   = "ANY"
    authorization = var.authorization_type
    authorizer_id = var.authorization_type == "CUSTOM" ? aws_api_gateway_authorizer.main[0].id : null
    api_key_required = var.api_key_required
    }

    # Lambda Integration
    resource "aws_api_gateway_integration" "lambda" {
    rest_api_id = aws_api_gateway_rest_api.main.id
    resource_id = aws_api_gateway_method.proxy.resource_id
    http_method = aws_api_gateway_method.proxy.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = var.lambda_invoke_arn
    }

    # CORS Configuration
    resource "aws_api_gateway_method" "proxy_options" {
    rest_api_id   = aws_api_gateway_rest_api.main.id
    resource_id   = aws_api_gateway_resource.proxy.id
    http_method   = "OPTIONS"
    authorization = "NONE"
    }

    resource "aws_api_gateway_integration" "proxy_options" {
    rest_api_id = aws_api_gateway_rest_api.main.id
    resource_id = aws_api_gateway_resource.proxy.id
    http_method = aws_api_gateway_method.proxy_options.http_method
    type        = "MOCK"

    request_templates = {
        "application/json" = jsonencode({
        statusCode = 200
        })
    }
    }

    resource "aws_api_gateway_method_response" "proxy_options" {
    rest_api_id = aws_api_gateway_rest_api.main.id
    resource_id = aws_api_gateway_resource.proxy.id
    http_method = aws_api_gateway_method.proxy_options.http_method
    status_code = "200"

    response_parameters = {
        "method.response.header.Access-Control-Allow-Headers" = true
        "method.response.header.Access-Control-Allow-Methods" = true
        "method.response.header.Access-Control-Allow-Origin"  = true
    }
    }

    resource "aws_api_gateway_integration_response" "proxy_options" {
    rest_api_id = aws_api_gateway_rest_api.main.id
    resource_id = aws_api_gateway_resource.proxy.id
    http_method = aws_api_gateway_method.proxy_options.http_method
    status_code = aws_api_gateway_method_response.proxy_options.status_code

    response_parameters = {
        "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
        "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT,DELETE'"
        "method.response.header.Access-Control-Allow-Origin"  = "'*'"
    }
    }

    # API Gateway Deployment
    resource "aws_api_gateway_deployment" "main" {
    depends_on = [
        aws_api_gateway_integration.lambda,
        aws_api_gateway_integration.proxy_options
    ]

    rest_api_id = aws_api_gateway_rest_api.main.id
    stage_name  = var.stage_name

    variables = {
        deployed_at = timestamp()
    }

    lifecycle {
        create_before_destroy = true
    }
    }

    # Custom Authorizer (optional)
    resource "aws_api_gateway_authorizer" "main" {
    count = var.authorization_type == "CUSTOM" ? 1 : 0

    name                   = "${var.environment}-${var.api_name}-authorizer"
    rest_api_id            = aws_api_gateway_rest_api.main.id
    authorizer_uri         = var.authorizer_lambda_arn
    authorizer_credentials = aws_iam_role.authorizer[0].arn
    type                   = "TOKEN"
    }

    # IAM Role for Custom Authorizer
    resource "aws_iam_role" "authorizer" {
    count = var.authorization_type == "CUSTOM" ? 1 : 0
    name  = "${var.environment}-${var.api_name}-authorizer-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "apigateway.amazonaws.com"
            }
        }
        ]
    })
    }

    resource "aws_iam_role_policy" "authorizer" {
    count = var.authorization_type == "CUSTOM" ? 1 : 0
    name  = "${var.environment}-${var.api_name}-authorizer-policy"
    role  = aws_iam_role.authorizer[0].id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action   = "lambda:InvokeFunction"
            Effect   = "Allow"
            Resource = var.authorizer_lambda_arn
        }
        ]
    })
    }

    # API Key (optional)
    resource "aws_api_gateway_api_key" "main" {
    count = var.create_api_key ? 1 : 0
    name  = "${var.environment}-${var.api_name}-key"

    tags = var.common_tags
    }

    # Usage Plan
    resource "aws_api_gateway_usage_plan" "main" {
    count = var.create_api_key ? 1 : 0
    name  = "${var.environment}-${var.api_name}-usage-plan"

    api_stages {
        api_id = aws_api_gateway_rest_api.main.id
        stage  = aws_api_gateway_deployment.main.stage_name
    }

    quota_settings {
        limit  = var.quota_limit
        period = var.quota_period
    }

    throttle_settings {
        rate_limit  = var.throttle_rate_limit
        burst_limit = var.throttle_burst_limit
    }

    tags = var.common_tags
    }

    resource "aws_api_gateway_usage_plan_key" "main" {
    count         = var.create_api_key ? 1 : 0
    key_id        = aws_api_gateway_api_key.main[0].id
    key_type      = "API_KEY"
    usage_plan_id = aws_api_gateway_usage_plan.main[0].id
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "api_name" {
    description = "Name of the API Gateway"
    type        = string
    }

    variable "api_description" {
    description = "Description of the API Gateway"
    type        = string
    default     = "REST API Gateway"
    }

    variable "endpoint_type" {
    description = "API Gateway endpoint type"
    type        = string
    default     = "REGIONAL"
    validation {
        condition     = contains(["EDGE", "REGIONAL", "PRIVATE"], var.endpoint_type)
        error_message = "Endpoint type must be EDGE, REGIONAL, or PRIVATE."
    }
    }

    variable "stage_name" {
    description = "Deployment stage name"
    type        = string
    default     = "prod"
    }

    variable "authorization_type" {
    description = "Authorization type for the method"
    type        = string
    default     = "NONE"
    validation {
        condition     = contains(["NONE", "AWS_IAM", "CUSTOM", "COGNITO_USER_POOLS"], var.authorization_type)
        error_message = "Authorization type must be NONE, AWS_IAM, CUSTOM, or COGNITO_USER_POOLS."
    }
    }

    variable "api_key_required" {
    description = "Whether API key is required"
    type        = bool
    default     = false
    }

    variable "lambda_invoke_arn" {
    description = "Lambda function invoke ARN"
    type        = string
    }

    variable "authorizer_lambda_arn" {
    description = "Custom authorizer Lambda ARN"
    type        = string
    default     = null
    }

    variable "create_api_key" {
    description = "Create API key and usage plan"
    type        = bool
    default     = false
    }

    variable "quota_limit" {
    description = "Usage plan quota limit"
    type        = number
    default     = 1000
    }

    variable "quota_period" {
    description = "Usage plan quota period"
    type        = string
    default     = "MONTH"
    }

    variable "throttle_rate_limit" {
    description = "Throttle rate limit"
    type        = number
    default     = 100
    }

    variable "throttle_burst_limit" {
    description = "Throttle burst limit"
    type        = number
    default     = 200
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "api_gateway_id" {
    description = "API Gateway REST API ID"
    value       = aws_api_gateway_rest_api.main.id
    }

    output "api_gateway_arn" {
    description = "API Gateway REST API ARN"
    value       = aws_api_gateway_rest_api.main.arn
    }

    output "api_gateway_execution_arn" {
    description = "API Gateway execution ARN"
    value       = aws_api_gateway_rest_api.main.execution_arn
    }

    output "api_gateway_invoke_url" {
    description = "API Gateway invoke URL"
    value       = aws_api_gateway_deployment.main.invoke_url
    }

    output "api_key_id" {
    description = "API Key ID"
    value       = var.create_api_key ? aws_api_gateway_api_key.main[0].id : null
    }

    output "usage_plan_id" {
    description = "Usage Plan ID"
    value       = var.create_api_key ? aws_api_gateway_usage_plan.main[0].id : null
    }'''
        }

    def _get_sqs_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# SQS Queue
    resource "aws_sqs_queue" "main" {
    name                       = "${var.environment}-${var.queue_name}"
    delay_seconds              = var.delay_seconds
    max_message_size           = var.max_message_size
    message_retention_seconds  = var.message_retention_seconds
    receive_wait_time_seconds  = var.receive_wait_time_seconds
    visibility_timeout_seconds = var.visibility_timeout_seconds

    # KMS encryption
    kms_master_key_id                 = var.kms_master_key_id
    kms_data_key_reuse_period_seconds = var.kms_data_key_reuse_period_seconds

    # Dead Letter Queue
    redrive_policy = var.create_dlq ? jsonencode({
        deadLetterTargetArn = aws_sqs_queue.dlq[0].arn
        maxReceiveCount     = var.max_receive_count
    }) : null

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.queue_name}"
    })
    }

    # Dead Letter Queue
    resource "aws_sqs_queue" "dlq" {
    count = var.create_dlq ? 1 : 0
    name  = "${var.environment}-${var.queue_name}-dlq"

    kms_master_key_id                 = var.kms_master_key_id
    kms_data_key_reuse_period_seconds = var.kms_data_key_reuse_period_seconds

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.queue_name}-dlq"
    })
    }

    # SQS Queue Policy
    resource "aws_sqs_queue_policy" "main" {
    count     = length(var.allowed_principals) > 0 ? 1 : 0
    queue_url = aws_sqs_queue.main.id

    policy = jsonencode({
        Version = "2012-10-17"
        Id      = "${aws_sqs_queue.main.arn}/SQSDefaultPolicy"
        Statement = [
        {
            Sid    = "AllowPrincipals"
            Effect = "Allow"
            Principal = {
            AWS = var.allowed_principals
            }
            Action = [
            "sqs:SendMessage",
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
            ]
            Resource = aws_sqs_queue.main.arn
        }
        ]
    })
    }

    # CloudWatch Alarms
    resource "aws_cloudwatch_metric_alarm" "queue_depth" {
    count = var.create_alarms ? 1 : 0

    alarm_name          = "${var.environment}-${var.queue_name}-depth"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods  = "2"
    metric_name         = "ApproximateNumberOfVisibleMessages"
    namespace           = "AWS/SQS"
    period              = "300"
    statistic           = "Average"
    threshold           = var.alarm_queue_depth_threshold
    alarm_description   = "This metric monitors SQS queue depth"
    alarm_actions       = var.alarm_sns_topic_arn != null ? [var.alarm_sns_topic_arn] : []

    dimensions = {
        QueueName = aws_sqs_queue.main.name
    }

    tags = var.common_tags
    }

    resource "aws_cloudwatch_metric_alarm" "dlq_depth" {
    count = var.create_dlq && var.create_alarms ? 1 : 0

    alarm_name          = "${var.environment}-${var.queue_name}-dlq-depth"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods  = "1"
    metric_name         = "ApproximateNumberOfVisibleMessages"
    namespace           = "AWS/SQS"
    period              = "300"
    statistic           = "Average"
    threshold           = "0"
    alarm_description   = "This metric monitors SQS DLQ depth"
    alarm_actions       = var.alarm_sns_topic_arn != null ? [var.alarm_sns_topic_arn] : []

    dimensions = {
        QueueName = aws_sqs_queue.dlq[0].name
    }

    tags = var.common_tags
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "queue_name" {
    description = "Name of the SQS queue"
    type        = string
    }

    variable "delay_seconds" {
    description = "Delay seconds for message delivery"
    type        = number
    default     = 0
    }

    variable "max_message_size" {
    description = "Maximum message size in bytes"
    type        = number
    default     = 262144
    }

    variable "message_retention_seconds" {
    description = "Message retention period in seconds"
    type        = number
    default     = 1209600
    }

    variable "receive_wait_time_seconds" {
    description = "Long polling wait time in seconds"
    type        = number
    default     = 0
    }

    variable "visibility_timeout_seconds" {
    description = "Visibility timeout in seconds"
    type        = number
    default     = 30
    }

    variable "kms_master_key_id" {
    description = "KMS key ID for encryption"
    type        = string
    default     = "alias/aws/sqs"
    }

    variable "kms_data_key_reuse_period_seconds" {
    description = "KMS data key reuse period"
    type        = number
    default     = 300
    }

    variable "create_dlq" {
    description = "Create dead letter queue"
    type        = bool
    default     = true
    }

    variable "max_receive_count" {
    description = "Maximum receive count before moving to DLQ"
    type        = number
    default     = 3
    }

    variable "allowed_principals" {
    description = "List of allowed principals for queue access"
    type        = list(string)
    default     = []
    }

    variable "create_alarms" {
    description = "Create CloudWatch alarms"
    type        = bool
    default     = true
    }

    variable "alarm_queue_depth_threshold" {
    description = "Threshold for queue depth alarm"
    type        = number
    default     = 100
    }

    variable "alarm_sns_topic_arn" {
    description = "SNS topic ARN for alarm notifications"
    type        = string
    default     = null
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "queue_id" {
    description = "SQS queue ID"
    value       = aws_sqs_queue.main.id
    }

    output "queue_arn" {
    description = "SQS queue ARN"
    value       = aws_sqs_queue.main.arn
    }

    output "queue_url" {
    description = "SQS queue URL"
    value       = aws_sqs_queue.main.url
    }

    output "queue_name" {
    description = "SQS queue name"
    value       = aws_sqs_queue.main.name
    }

    output "dlq_id" {
    description = "Dead letter queue ID"
    value       = var.create_dlq ? aws_sqs_queue.dlq[0].id : null
    }

    output "dlq_arn" {
    description = "Dead letter queue ARN"
    value       = var.create_dlq ? aws_sqs_queue.dlq[0].arn : null
    }

    output "dlq_url" {
    description = "Dead letter queue URL"
    value       = var.create_dlq ? aws_sqs_queue.dlq[0].url : null
    }'''
        }

    def _get_sns_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# SNS Topic
    resource "aws_sns_topic" "main" {
    name         = "${var.environment}-${var.topic_name}"
    display_name = var.display_name

    # KMS encryption
    kms_master_key_id = var.kms_master_key_id

    # Delivery policy
    delivery_policy = var.delivery_policy

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.topic_name}"
    })
    }

    # SNS Topic Policy
    resource "aws_sns_topic_policy" "main" {
    count = length(var.allowed_principals) > 0 ? 1 : 0
    arn   = aws_sns_topic.main.arn

    policy = jsonencode({
        Version = "2012-10-17"
        Id      = "${aws_sns_topic.main.arn}/SNSDefaultPolicy"
        Statement = [
        {
            Sid    = "AllowPrincipals"
            Effect = "Allow"
            Principal = {
            AWS = var.allowed_principals
            }
            Action = [
            "sns:Publish",
            "sns:GetTopicAttributes",
            "sns:SetTopicAttributes",
            "sns:AddPermission",
            "sns:RemovePermission",
            "sns:DeleteTopic",
            "sns:Subscribe",
            "sns:ListSubscriptionsByTopic"
            ]
            Resource = aws_sns_topic.main.arn
        }
        ]
    })
    }

    # Email Subscriptions
    resource "aws_sns_topic_subscription" "email" {
    count = length(var.email_subscriptions)

    topic_arn = aws_sns_topic.main.arn
    protocol  = "email"
    endpoint  = var.email_subscriptions[count.index]
    }

    # SMS Subscriptions
    resource "aws_sns_topic_subscription" "sms" {
    count = length(var.sms_subscriptions)

    topic_arn = aws_sns_topic.main.arn
    protocol  = "sms"
    endpoint  = var.sms_subscriptions[count.index]
    }

    # Lambda Subscriptions
    resource "aws_sns_topic_subscription" "lambda" {
    count = length(var.lambda_subscriptions)

    topic_arn = aws_sns_topic.main.arn
    protocol  = "lambda"
    endpoint  = var.lambda_subscriptions[count.index].arn

    filter_policy = var.lambda_subscriptions[count.index].filter_policy
    }

    # Lambda permissions for SNS
    resource "aws_lambda_permission" "sns" {
    count = length(var.lambda_subscriptions)

    statement_id  = "AllowExecutionFromSNS-${count.index}"
    action        = "lambda:InvokeFunction"
    function_name = var.lambda_subscriptions[count.index].arn
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.main.arn
    }

    # SQS Subscriptions
    resource "aws_sns_topic_subscription" "sqs" {
    count = length(var.sqs_subscriptions)

    topic_arn = aws_sns_topic.main.arn
    protocol  = "sqs"
    endpoint  = var.sqs_subscriptions[count.index].arn

    filter_policy = var.sqs_subscriptions[count.index].filter_policy
    }

    # SQS queue policies for SNS
    resource "aws_sqs_queue_policy" "sns" {
    count     = length(var.sqs_subscriptions)
    queue_url = var.sqs_subscriptions[count.index].url

    policy = jsonencode({
        Version = "2012-10-17"
        Id      = "${var.sqs_subscriptions[count.index].arn}/SNStoSQSPolicy"
        Statement = [
        {
            Sid    = "AllowSNSMessages"
            Effect = "Allow"
            Principal = {
            Service = "sns.amazonaws.com"
            }
            Action   = "sqs:SendMessage"
            Resource = var.sqs_subscriptions[count.index].arn
            Condition = {
            ArnEquals = {
                "aws:SourceArn" = aws_sns_topic.main.arn
            }
            }
        }
        ]
    })
    }

    # HTTP/HTTPS Subscriptions
    resource "aws_sns_topic_subscription" "http" {
    count = length(var.http_subscriptions)

    topic_arn = aws_sns_topic.main.arn
    protocol  = var.http_subscriptions[count.index].protocol
    endpoint  = var.http_subscriptions[count.index].endpoint

    filter_policy = var.http_subscriptions[count.index].filter_policy
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "topic_name" {
    description = "Name of the SNS topic"
    type        = string
    }

    variable "display_name" {
    description = "Display name for the SNS topic"
    type        = string
    default     = null
    }

    variable "kms_master_key_id" {
    description = "KMS key ID for encryption"
    type        = string
    default     = "alias/aws/sns"
    }

    variable "delivery_policy" {
    description = "SNS delivery policy"
    type        = string
    default     = null
    }

    variable "allowed_principals" {
    description = "List of allowed principals for topic access"
    type        = list(string)
    default     = []
    }

    variable "email_subscriptions" {
    description = "List of email addresses to subscribe"
    type        = list(string)
    default     = []
    }

    variable "sms_subscriptions" {
    description = "List of phone numbers to subscribe"
    type        = list(string)
    default     = []
    }

    variable "lambda_subscriptions" {
    description = "List of Lambda function subscriptions"
    type = list(object({
        arn           = string
        filter_policy = string
    }))
    default = []
    }

    variable "sqs_subscriptions" {
    description = "List of SQS queue subscriptions"
    type = list(object({
        arn           = string
        url           = string
        filter_policy = string
    }))
    default = []
    }

    variable "http_subscriptions" {
    description = "List of HTTP/HTTPS subscriptions"
    type = list(object({
        protocol      = string
        endpoint      = string
        filter_policy = string
    }))
    default = []
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "topic_arn" {
    description = "SNS topic ARN"
    value       = aws_sns_topic.main.arn
    }

    output "topic_id" {
    description = "SNS topic ID"
    value       = aws_sns_topic.main.id
    }

    output "topic_name" {
    description = "SNS topic name"
    value       = aws_sns_topic.main.name
    }

    output "email_subscription_arns" {
    description = "Email subscription ARNs"
    value       = aws_sns_topic_subscription.email[*].arn
    }

    output "sms_subscription_arns" {
    description = "SMS subscription ARNs"
    value       = aws_sns_topic_subscription.sms[*].arn
    }

    output "lambda_subscription_arns" {
    description = "Lambda subscription ARNs"
    value       = aws_sns_topic_subscription.lambda[*].arn
    }

    output "sqs_subscription_arns" {
    description = "SQS subscription ARNs"
    value       = aws_sns_topic_subscription.sqs[*].arn
    }'''
        }
# Add these methods to your GitHubPatternFetcher class

    def get_pattern_code(self, pattern: TerraformPattern) -> Dict[str, str]:
        """Generate sample code for a pattern"""
        if "VPC" in pattern.name:
            return self._get_vpc_code()
        elif "EC2" in pattern.name:
            return self._get_ec2_code()
        elif "RDS" in pattern.name:
            return self._get_rds_code()
        elif "S3" in pattern.name:
            return self._get_s3_code()
        elif "Application Load Balancer" in pattern.name:
            return self._get_alb_code()
        elif "EKS" in pattern.name:
            return self._get_eks_code()
        # New patterns
        elif "Lambda" in pattern.name:
            return self._get_lambda_code()
        elif "Auto Scaling" in pattern.name:
            return self._get_asg_code()
        elif "CloudFront" in pattern.name:
            return self._get_cloudfront_code()
        elif "API Gateway" in pattern.name:
            return self._get_api_gateway_code()
        elif "SQS" in pattern.name:
            return self._get_sqs_code()
        elif "SNS" in pattern.name:
            return self._get_sns_code()
        elif "IAM" in pattern.name:
            return self._get_iam_code()
        elif "Secrets Manager" in pattern.name:
            return self._get_secrets_manager_code()
        elif "CloudWatch" in pattern.name:
            return self._get_cloudwatch_code()
        elif "DynamoDB" in pattern.name:
            return self._get_dynamodb_code()
        elif "ElastiCache" in pattern.name:
            return self._get_elasticache_code()
        elif "Route53" in pattern.name:
            return self._get_route53_code()
        elif "Security Groups" in pattern.name:
            return self._get_security_groups_code()
        elif "3-Tier" in pattern.name:
            return self._get_three_tier_code()
        elif "Serverless Web" in pattern.name:
            return self._get_serverless_webapp_code()
        else:
            return self._get_basic_code(pattern.name)

    def _get_lambda_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# Lambda Function
    resource "aws_lambda_function" "main" {
    filename         = var.lambda_zip_path
    function_name    = "${var.environment}-${var.function_name}"
    role            = aws_iam_role.lambda.arn
    handler         = var.handler
    source_code_hash = filebase64sha256(var.lambda_zip_path)
    runtime         = var.runtime
    timeout         = var.timeout
    memory_size     = var.memory_size

    environment {
        variables = var.environment_variables
    }

    vpc_config {
        subnet_ids         = var.subnet_ids
        security_group_ids = var.security_group_ids
    }

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.function_name}"
    })
    }

    # IAM Role for Lambda
    resource "aws_iam_role" "lambda" {
    name = "${var.environment}-${var.function_name}-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "lambda.amazonaws.com"
            }
        }
        ]
    })

    tags = var.common_tags
    }

    # Basic Lambda execution policy
    resource "aws_iam_role_policy_attachment" "lambda_basic" {
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    role       = aws_iam_role.lambda.name
    }

    # VPC execution policy (if VPC is used)
    resource "aws_iam_role_policy_attachment" "lambda_vpc" {
    count      = length(var.subnet_ids) > 0 ? 1 : 0
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    role       = aws_iam_role.lambda.name
    }

    # CloudWatch Log Group
    resource "aws_cloudwatch_log_group" "lambda" {
    name              = "/aws/lambda/${var.environment}-${var.function_name}"
    retention_in_days = var.log_retention_days

    tags = var.common_tags
    }

    # Lambda Permission for API Gateway (optional)
    resource "aws_lambda_permission" "api_gateway" {
    count         = var.enable_api_gateway ? 1 : 0
    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.main.function_name
    principal     = "apigateway.amazonaws.com"
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "function_name" {
    description = "Lambda function name"
    type        = string
    }

    variable "lambda_zip_path" {
    description = "Path to Lambda deployment package"
    type        = string
    default     = "lambda_function.zip"
    }

    variable "handler" {
    description = "Lambda function handler"
    type        = string
    default     = "index.handler"
    }

    variable "runtime" {
    description = "Lambda runtime"
    type        = string
    default     = "python3.9"
    }

    variable "timeout" {
    description = "Lambda timeout in seconds"
    type        = number
    default     = 30
    }

    variable "memory_size" {
    description = "Lambda memory size in MB"
    type        = number
    default     = 128
    }

    variable "environment_variables" {
    description = "Environment variables for Lambda"
    type        = map(string)
    default     = {}
    }

    variable "subnet_ids" {
    description = "Subnet IDs for VPC configuration"
    type        = list(string)
    default     = []
    }

    variable "security_group_ids" {
    description = "Security group IDs for VPC configuration"
    type        = list(string)
    default     = []
    }

    variable "log_retention_days" {
    description = "CloudWatch log retention period"
    type        = number
    default     = 14
    }

    variable "enable_api_gateway" {
    description = "Enable API Gateway integration"
    type        = bool
    default     = false
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "lambda_function_arn" {
    description = "Lambda function ARN"
    value       = aws_lambda_function.main.arn
    }

    output "lambda_function_name" {
    description = "Lambda function name"
    value       = aws_lambda_function.main.function_name
    }

    output "lambda_invoke_arn" {
    description = "Lambda function invoke ARN"
    value       = aws_lambda_function.main.invoke_arn
    }

    output "lambda_role_arn" {
    description = "Lambda IAM role ARN"
    value       = aws_iam_role.lambda.arn
    }

    output "cloudwatch_log_group" {
    description = "CloudWatch log group name"
    value       = aws_cloudwatch_log_group.lambda.name
    }'''
        }

    
    
    
    def _get_asg_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# Launch Template
    resource "aws_launch_template" "main" {
    name_prefix   = "${var.environment}-${var.name}-"
    image_id      = data.aws_ami.amazon_linux.id
    instance_type = var.instance_type
    key_name      = var.key_name

    vpc_security_group_ids = [aws_security_group.asg.id]

    user_data = base64encode(templatefile("${path.module}/user_data.sh", {
        environment = var.environment
    }))

    block_device_mappings {
        device_name = "/dev/xvda"
        ebs {
        volume_size = var.root_volume_size
        volume_type = "gp3"
        encrypted   = true
        }
    }

    iam_instance_profile {
        name = aws_iam_instance_profile.main.name
    }

    tag_specifications {
        resource_type = "instance"
        tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.name}"
        })
    }

    tags = var.common_tags
    }

    # Auto Scaling Group
    resource "aws_autoscaling_group" "main" {
    name                = "${var.environment}-${var.name}-asg"
    vpc_zone_identifier = var.subnet_ids
    target_group_arns   = var.target_group_arns
    health_check_type   = var.health_check_type
    health_check_grace_period = var.health_check_grace_period

    min_size         = var.min_size
    max_size         = var.max_size
    desired_capacity = var.desired_capacity

    launch_template {
        id      = aws_launch_template.main.id
        version = "$Latest"
    }

    enabled_metrics = var.enabled_metrics

    dynamic "tag" {
        for_each = var.common_tags
        content {
        key                 = tag.key
        value               = tag.value
        propagate_at_launch = true
        }
    }

    tag {
        key                 = "Name"
        value               = "${var.environment}-${var.name}"
        propagate_at_launch = true
    }
    }

    # Security Group
    resource "aws_security_group" "asg" {
    name_prefix = "${var.environment}-${var.name}-asg-"
    vpc_id      = var.vpc_id

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = var.allowed_cidrs
    }

    ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = var.allowed_cidrs
    }

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = var.ssh_allowed_cidrs
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.name}-asg-sg"
    })
    }

    # IAM Instance Profile
    resource "aws_iam_instance_profile" "main" {
    name = "${var.environment}-${var.name}-profile"
    role = aws_iam_role.main.name
    }

    resource "aws_iam_role" "main" {
    name = "${var.environment}-${var.name}-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "ec2.amazonaws.com"
            }
        }
        ]
    })

    tags = var.common_tags
    }

    # CloudWatch Agent policy
    resource "aws_iam_role_policy_attachment" "cloudwatch_agent" {
    policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
    role       = aws_iam_role.main.name
    }

    # SSM policy for Systems Manager
    resource "aws_iam_role_policy_attachment" "ssm_managed" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
    role       = aws_iam_role.main.name
    }

    # Data source for latest Amazon Linux 2 AMI
    data "aws_ami" "amazon_linux" {
    most_recent = true
    owners      = ["amazon"]

    filter {
        name   = "name"
        values = ["amzn2-ami-hvm-*-x86_64-gp2"]
    }
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "name" {
    description = "Name for the Auto Scaling Group"
    type        = string
    default     = "web"
    }

    variable "vpc_id" {
    description = "VPC ID"
    type        = string
    }

    variable "subnet_ids" {
    description = "Subnet IDs for the Auto Scaling Group"
    type        = list(string)
    }

    variable "instance_type" {
    description = "EC2 instance type"
    type        = string
    default     = "t3.micro"
    }

    variable "key_name" {
    description = "EC2 Key Pair name"
    type        = string
    }

    variable "min_size" {
    description = "Minimum number of instances"
    type        = number
    default     = 1
    }

    variable "max_size" {
    description = "Maximum number of instances"
    type        = number
    default     = 3
    }

    variable "desired_capacity" {
    description = "Desired number of instances"
    type        = number
    default     = 2
    }

    variable "target_group_arns" {
    description = "Target group ARNs for load balancer"
    type        = list(string)
    default     = []
    }

    variable "health_check_type" {
    description = "Health check type (EC2 or ELB)"
    type        = string
    default     = "ELB"
    }

    variable "health_check_grace_period" {
    description = "Health check grace period"
    type        = number
    default     = 300
    }

    variable "root_volume_size" {
    description = "Root volume size in GB"
    type        = number
    default     = 20
    }

    variable "allowed_cidrs" {
    description = "CIDR blocks allowed for HTTP/HTTPS access"
    type        = list(string)
    default     = ["0.0.0.0/0"]
    }

    variable "ssh_allowed_cidrs" {
    description = "CIDR blocks allowed for SSH access"
    type        = list(string)
    default     = ["10.0.0.0/8"]
    }

    variable "enabled_metrics" {
    description = "List of enabled ASG metrics"
    type        = list(string)
    default = [
        "GroupMinSize",
        "GroupMaxSize",
        "GroupDesiredCapacity",
        "GroupInServiceInstances",
        "GroupTotalInstances"
    ]
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "autoscaling_group_id" {
    description = "Auto Scaling Group ID"
    value       = aws_autoscaling_group.main.id
    }

    output "autoscaling_group_arn" {
    description = "Auto Scaling Group ARN"
    value       = aws_autoscaling_group.main.arn
    }

    output "launch_template_id" {
    description = "Launch Template ID"
    value       = aws_launch_template.main.id
    }

    output "security_group_id" {
    description = "Security Group ID"
    value       = aws_security_group.asg.id
    }

    output "iam_role_arn" {
    description = "IAM Role ARN"
    value       = aws_iam_role.main.arn
    }'''
        }

    def _get_cloudfront_code(self) -> Dict[str, str]:
        return {
            "main.tf": '''# S3 Bucket for CloudFront Origin (optional)
    resource "aws_s3_bucket" "origin" {
    count  = var.create_s3_origin ? 1 : 0
    bucket = var.origin_bucket_name

    tags = merge(var.common_tags, {
        Name = var.origin_bucket_name
    })
    }

    resource "aws_s3_bucket_versioning" "origin" {
    count  = var.create_s3_origin ? 1 : 0
    bucket = aws_s3_bucket.origin[0].id
    versioning_configuration {
        status = "Enabled"
    }
    }

    resource "aws_s3_bucket_server_side_encryption_configuration" "origin" {
    count  = var.create_s3_origin ? 1 : 0
    bucket = aws_s3_bucket.origin[0].id

    rule {
        apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
        }
    }
    }

    # Origin Access Control
    resource "aws_cloudfront_origin_access_control" "main" {
    count                             = var.create_s3_origin ? 1 : 0
    name                              = "${var.environment}-${var.distribution_name}-oac"
    description                       = "OAC for ${var.distribution_name}"
    origin_access_control_origin_type = "s3"
    signing_behavior                  = "always"
    signing_protocol                  = "sigv4"
    }

    # CloudFront Distribution
    resource "aws_cloudfront_distribution" "main" {
    origin {
        domain_name              = var.create_s3_origin ? aws_s3_bucket.origin[0].bucket_regional_domain_name : var.origin_domain_name
        origin_id                = var.origin_id
        origin_access_control_id = var.create_s3_origin ? aws_cloudfront_origin_access_control.main[0].id : null

        dynamic "custom_origin_config" {
        for_each = var.create_s3_origin ? [] : [1]
        content {
            http_port              = var.origin_http_port
            https_port             = var.origin_https_port
            origin_protocol_policy = var.origin_protocol_policy
            origin_ssl_protocols   = var.origin_ssl_protocols
        }
        }
    }

    enabled             = true
    is_ipv6_enabled     = var.ipv6_enabled
    comment             = var.comment
    default_root_object = var.default_root_object

    aliases = var.aliases

    default_cache_behavior {
        allowed_methods  = var.allowed_methods
        cached_methods   = var.cached_methods
        target_origin_id = var.origin_id

        forwarded_values {
        query_string = var.forward_query_string
        cookies {
            forward = var.forward_cookies
        }
        headers = var.forward_headers
        }

        viewer_protocol_policy = var.viewer_protocol_policy
        min_ttl                = var.min_ttl
        default_ttl            = var.default_ttl
        max_ttl                = var.max_ttl
        compress               = var.compress
    }

    # Custom error responses
    dynamic "custom_error_response" {
        for_each = var.custom_error_responses
        content {
        error_code            = custom_error_response.value.error_code
        response_code         = custom_error_response.value.response_code
        response_page_path    = custom_error_response.value.response_page_path
        error_caching_min_ttl = custom_error_response.value.error_caching_min_ttl
        }
    }

    price_class = var.price_class

    restrictions {
        geo_restriction {
        restriction_type = var.geo_restriction_type
        locations        = var.geo_restriction_locations
        }
    }

    viewer_certificate {
        cloudfront_default_certificate = var.use_default_certificate
        acm_certificate_arn            = var.ssl_certificate_arn
        ssl_support_method             = var.ssl_certificate_arn != null ? "sni-only" : null
        minimum_protocol_version       = var.ssl_certificate_arn != null ? "TLSv1.2_2021" : null
    }

    web_acl_id = var.web_acl_id

    tags = merge(var.common_tags, {
        Name = "${var.environment}-${var.distribution_name}"
    })
    }

    # S3 Bucket Policy for CloudFront (if using S3 origin)
    resource "aws_s3_bucket_policy" "origin" {
    count  = var.create_s3_origin ? 1 : 0
    bucket = aws_s3_bucket.origin[0].id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Sid    = "AllowCloudFrontServicePrincipal"
            Effect = "Allow"
            Principal = {
            Service = "cloudfront.amazonaws.com"
            }
            Action   = "s3:GetObject"
            Resource = "${aws_s3_bucket.origin[0].arn}/*"
            Condition = {
            StringEquals = {
                "AWS:SourceArn" = aws_cloudfront_distribution.main.arn
            }
            }
        }
        ]
    })
    }''',
            "variables.tf": '''variable "environment" {
    description = "Environment name"
    type        = string
    default     = "dev"
    }

    variable "distribution_name" {
    description = "Name for the CloudFront distribution"
    type        = string
    }

    variable "create_s3_origin" {
    description = "Create S3 bucket as origin"
    type        = bool
    default     = true
    }

    variable "origin_bucket_name" {
    description = "S3 bucket name for origin (if creating)"
    type        = string
    default     = null
    }

    variable "origin_domain_name" {
    description = "Origin domain name (if not using S3)"
    type        = string
    default     = null
    }

    variable "origin_id" {
    description = "Origin ID"
    type        = string
    default     = "primary-origin"
    }

    variable "origin_http_port" {
    description = "HTTP port for custom origin"
    type        = number
    default     = 80
    }

    variable "origin_https_port" {
    description = "HTTPS port for custom origin"
    type        = number
    default     = 443
    }

    variable "origin_protocol_policy" {
    description = "Origin protocol policy"
    type        = string
    default     = "https-only"
    }

    variable "origin_ssl_protocols" {
    description = "SSL protocols for origin"
    type        = list(string)
    default     = ["TLSv1.2"]
    }

    variable "aliases" {
    description = "Alternate domain names (CNAMEs)"
    type        = list(string)
    default     = []
    }

    variable "comment" {
    description = "Comment for the distribution"
    type        = string
    default     = "CloudFront Distribution"
    }

    variable "default_root_object" {
    description = "Default root object"
    type        = string
    default     = "index.html"
    }

    variable "ipv6_enabled" {
    description = "Enable IPv6"
    type        = bool
    default     = true
    }

    variable "allowed_methods" {
    description = "Allowed HTTP methods"
    type        = list(string)
    default     = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    }

    variable "cached_methods" {
    description = "Cached HTTP methods"
    type        = list(string)
    default     = ["GET", "HEAD"]
    }

    variable "viewer_protocol_policy" {
    description = "Viewer protocol policy"
    type        = string
    default     = "redirect-to-https"
    }

    variable "forward_query_string" {
    description = "Forward query strings"
    type        = bool
    default     = false
    }

    variable "forward_cookies" {
    description = "Forward cookies policy"
    type        = string
    default     = "none"
    }

    variable "forward_headers" {
    description = "Headers to forward to origin"
    type        = list(string)
    default     = []
    }

    variable "min_ttl" {
    description = "Minimum TTL"
    type        = number
    default     = 0
    }

    variable "default_ttl" {
    description = "Default TTL"
    type        = number
    default     = 3600
    }

    variable "max_ttl" {
    description = "Maximum TTL"
    type        = number
    default     = 86400
    }

    variable "compress" {
    description = "Enable compression"
    type        = bool
    default     = true
    }

    variable "price_class" {
    description = "Price class for the distribution"
    type        = string
    default     = "PriceClass_100"
    }

    variable "geo_restriction_type" {
    description = "Geo restriction type"
    type        = string
    default     = "none"
    }

    variable "geo_restriction_locations" {
    description = "Geo restriction locations"
    type        = list(string)
    default     = []
    }

    variable "use_default_certificate" {
    description = "Use default CloudFront certificate"
    type        = bool
    default     = true
    }

    variable "ssl_certificate_arn" {
    description = "ACM certificate ARN for custom SSL"
    type        = string
    default     = null
    }

    variable "web_acl_id" {
    description = "WAF Web ACL ID"
    type        = string
    default     = null
    }

    variable "custom_error_responses" {
    description = "Custom error response configuration"
    type = list(object({
        error_code            = number
        response_code         = number
        response_page_path    = string
        error_caching_min_ttl = number
    }))
    default = []
    }

    variable "common_tags" {
    description = "Common tags for all resources"
    type        = map(string)
    default = {
        Terraform   = "true"
        Environment = "dev"
    }
    }''',
            "outputs.tf": '''output "cloudfront_distribution_id" {
    description = "CloudFront Distribution ID"
    value       = aws_cloudfront_distribution.main.id
    }

    output "cloudfront_distribution_arn" {
    description = "CloudFront Distribution ARN"
    value       = aws_cloudfront_distribution.main.arn
    }

    output "cloudfront_domain_name" {
    description = "CloudFront Distribution domain name"
    value       = aws_cloudfront_distribution.main.domain_name
    }

    output "cloudfront_hosted_zone_id" {
    description = "CloudFront Distribution hosted zone ID"
    value       = aws_cloudfront_distribution.main.hosted_zone_id
    }

    output "origin_bucket_name" {
    description = "Origin S3 bucket name"
    value       = var.create_s3_origin ? aws_s3_bucket.origin[0].bucket : null
    }

    output "origin_bucket_arn" {
    description = "Origin S3 bucket ARN"
    value       = var.create_s3_origin ? aws_s3_bucket.origin[0].arn : null
    }'''
        }
    
    def _get_alb_code(self) -> Dict[str, str]:
        return self._get_basic_code("Application Load Balancer")
    
    def _get_nlb_code(self) -> Dict[str, str]:
        return self._get_basic_code("Network Load Balancer")
    
    def _get_eks_code(self) -> Dict[str, str]:
        return self._get_basic_code("EKS Cluster")
    
    def _get_ecs_code(self) -> Dict[str, str]:
        return self._get_basic_code("ECS Cluster")
    
    def _get_rds_code(self) -> Dict[str, str]:
        return self._get_basic_code("RDS Database")
    
    def _get_asg_code(self) -> Dict[str, str]:
        return self._get_basic_code("Auto Scaling Group")
    
    def _get_cloudfront_code(self) -> Dict[str, str]:
        return self._get_basic_code("CloudFront Distribution")
    
    def _get_api_gateway_code(self) -> Dict[str, str]:
        return self._get_basic_code("API Gateway")
    
    def _get_sqs_code(self) -> Dict[str, str]:
        return self._get_basic_code("SQS Queue")
    
    def _get_sns_code(self) -> Dict[str, str]:
        return self._get_basic_code("SNS Topic")
    
    def _get_dynamodb_code(self) -> Dict[str, str]:
        return self._get_basic_code("DynamoDB Table")
    
    def _get_elasticache_code(self) -> Dict[str, str]:
        return self._get_basic_code("ElastiCache Redis Cluster")
    
    def _get_route53_code(self) -> Dict[str, str]:
        return self._get_basic_code("Route53 DNS Configuration")
    
    def _get_iam_code(self) -> Dict[str, str]:
        return self._get_basic_code("IAM Roles and Policies")
    
    def _get_secrets_manager_code(self) -> Dict[str, str]:
        return self._get_basic_code("AWS Secrets Manager")
    
    def _get_parameter_store_code(self) -> Dict[str, str]:
        return self._get_basic_code("Systems Manager Parameter Store")
    
    def _get_cloudwatch_code(self) -> Dict[str, str]:
        return self._get_basic_code("CloudWatch Monitoring")
    
    def _get_ecr_code(self) -> Dict[str, str]:
        return self._get_basic_code("ECR Repository")
    
    def _get_codepipeline_code(self) -> Dict[str, str]:
        return self._get_basic_code("CodePipeline")
    
    def _get_efs_code(self) -> Dict[str, str]:
        return self._get_basic_code("EFS File System")
    
    def _get_nat_gateway_code(self) -> Dict[str, str]:
        return self._get_basic_code("NAT Gateway")
    
    def _get_security_groups_code(self) -> Dict[str, str]:
        return self._get_basic_code("Security Groups Configuration")
    
    def _get_three_tier_code(self) -> Dict[str, str]:
        return self._get_basic_code("3-Tier Web Application Architecture")
    
    def _get_serverless_webapp_code(self) -> Dict[str, str]:
        return self._get_basic_code("Serverless Web Application")
    
    def _get_data_lake_code(self) -> Dict[str, str]:
        return self._get_basic_code("Data Lake Architecture")
    
    
    def _get_basic_code(self, pattern_name: str) -> Dict[str, str]:
        return {
            "main.tf": f'''# {pattern_name} Configuration
# This is a basic template for {pattern_name}

terraform {{
  required_version = ">= 1.0"
  
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

# Add your {pattern_name} resources here''',
            "variables.tf": '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}''',
            "outputs.tf": '''# Add your outputs here
# Example:
# output "resource_id" {
#   description = "ID of the created resource"
#   value       = aws_resource.example.id
# }'''
        }

# Claude Code Generator Class
class ClaudeCodeGenerator:
    def __init__(self, api_key: str):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            st.error("Anthropic library not installed. Please add 'anthropic' to requirements.txt")
            self.client = None
    
    def generate_terraform_code(self, requirements: Dict) -> Dict:
        """Generate Terraform code based on user requirements"""
        if not self.client:
            return {}
        
        prompt = self._build_generation_prompt(requirements)
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            return self._parse_terraform_response(response.content[0].text)
        except Exception as e:
            st.error(f"Claude API error: {str(e)}")
            return {}
    
    def _build_generation_prompt(self, requirements: Dict) -> str:
        """Build comprehensive prompt for Terraform generation"""
        services_list = ', '.join(requirements.get('services', []))
        
        prompt = f"""
You are an expert Terraform engineer. Generate production-ready Terraform code based on these requirements:

**Infrastructure Requirements:**
- Cloud Provider: {requirements.get('provider', 'AWS')}
- Project Name: {requirements.get('project_name', 'infrastructure')}
- Services Needed: {services_list}
- Environment: {requirements.get('environment', 'development')}
- Region: {requirements.get('region', 'us-west-2')}

**Project Details:**
- Description: {requirements.get('description', 'Infrastructure deployment')}
- High Availability: {requirements.get('ha_required', False)}
- Backup Required: {requirements.get('backup_required', False)}
- Monitoring: {requirements.get('monitoring', False)}
- Auto Scaling: {requirements.get('auto_scaling', False)}

**Security & Compliance:**
- Compliance: {requirements.get('compliance', 'Standard')}
- Security Hardening: {requirements.get('security_hardening', True)}
- VPC Configuration: {requirements.get('vpc_config', 'Default')}

Please generate these files:
1. main.tf - Main resource definitions
2. variables.tf - Input variables with descriptions and defaults  
3. outputs.tf - Output values
4. versions.tf - Provider version constraints

Follow these best practices:
- Use consistent naming with {requirements.get('environment', 'dev')} prefix
- Include proper tags for resource management
- Implement security best practices
- Add comprehensive comments
- Use data sources where appropriate
- Include proper resource dependencies

Return your response in this exact JSON format:
{{
    "main.tf": "terraform code here",
    "variables.tf": "variables code here", 
    "outputs.tf": "outputs code here",
    "versions.tf": "versions code here"
}}
"""
        return prompt
    
    def _parse_terraform_response(self, response: str) -> Dict:
        """Parse Claude's response into structured Terraform files"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return self._create_fallback_response(response)
                
        except json.JSONDecodeError:
            return self._create_fallback_response(response)
    
    def _create_fallback_response(self, response: str) -> Dict:
        """Create fallback response if JSON parsing fails"""
        return {
            "main.tf": response,
            "variables.tf": '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}''',
            "outputs.tf": '''# Outputs will be defined based on created resources
# Example outputs:
# output "vpc_id" {
#   description = "VPC ID"
#   value       = aws_vpc.main.id
# }''',
            "versions.tf": '''terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = var.common_tags
  }
}'''
        }

# Utility Functions
def create_terraform_zip(files_dict: Dict[str, str]) -> bytes:
    """Create ZIP file from generated Terraform files"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in files_dict.items():
            zip_file.writestr(filename, content)
    
    zip_buffer.seek(0)
    return zip_buffer.read()

def generate_jenkins_pipeline(project_name: str, git_repo: str, tf_version: str, auto_approve: bool) -> str:
    """Generate Jenkins pipeline configuration"""
    auto_approve_flag = "-auto-approve" if auto_approve else ""
    
    return f"""pipeline {{
    agent any
    
    environment {{
        TERRAFORM_VERSION = '{tf_version}'
        PROJECT_NAME = '{project_name}'
        AWS_DEFAULT_REGION = 'us-west-2'
    }}
    
    stages {{
        stage('Checkout') {{
            steps {{
                git branch: 'main', url: '{git_repo}'
            }}
        }}
        
        stage('Terraform Init') {{
            steps {{
                sh '''
                    terraform --version
                    terraform init
                '''
            }}
        }}
        
        stage('Terraform Validate') {{
            steps {{
                sh 'terraform validate'
            }}
        }}
        
        stage('Terraform Plan') {{
            steps {{
                sh '''
                    terraform plan -out=tfplan
                    terraform show -no-color tfplan > tfplan.txt
                '''
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'tfplan.txt',
                    reportName: 'Terraform Plan'
                ])
            }}
        }}
        
        stage('Terraform Apply') {{
            when {{
                branch 'main'
            }}
            steps {{
                sh 'terraform apply {auto_approve_flag} tfplan'
            }}
        }}
    }}
    
    post {{
        always {{
            archiveArtifacts artifacts: '*.tf, *.tfvars, tfplan.txt', fingerprint: true
        }}
        
        failure {{
            emailext (
                subject: "Terraform Deploy Failed: {project_name}",
                body: "The Terraform deployment has failed. Please check the logs.",
                to: "${{env.CHANGE_AUTHOR_EMAIL}}"
            )
        }}
    }}
}}"""

# UI Components
def render_pattern_browser_updated():
    """Updated pattern browser with expanded categories"""
    st.header("🔍 Terraform Pattern Browser")
    st.markdown("Browse and download official Terraform patterns from curated repositories.")
    
    # Initialize fetcher
    github_token = st.secrets.get("GITHUB_TOKEN")
    fetcher = GitHubPatternFetcher(token=github_token)
    
    # Sidebar filters
    with st.sidebar:
        st.subheader("🔧 Filters")
        
        provider_filter = st.selectbox(
            "Cloud Provider",
            ["All", "AWS", "Azure", "GCP"]
        )
        
        category_filter = st.selectbox(
            "Category", 
            ["All", "compute", "storage", "networking", "database", "security", 
             "messaging", "monitoring", "devops", "architecture"]
        )
        
        complexity_filter = st.selectbox(
            "Complexity Level",
            ["All", "beginner", "intermediate", "advanced"]
        )
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Refresh Patterns", type="primary"):
            with st.spinner("Fetching latest patterns..."):
                patterns = fetcher.fetch_aws_patterns()
                
                # Apply filters
                if provider_filter != "All":
                    patterns = [p for p in patterns if p.provider.lower() == provider_filter.lower()]
                if category_filter != "All":
                    patterns = [p for p in patterns if p.category.lower() == category_filter.lower()]
                if complexity_filter != "All":
                    patterns = [p for p in patterns if p.complexity.lower() == complexity_filter.lower()]
                
                st.session_state.patterns = patterns
            st.success(f"Found {len(patterns)} patterns!")
    
    with col1:
        st.markdown("### Available Patterns")
    
    # Display patterns
    if 'patterns' in st.session_state:
        patterns = st.session_state.patterns
        
        if not patterns:
            st.warning("⚠️ No patterns found matching your criteria.")
            return
        
        for i, pattern in enumerate(patterns):
            with st.expander(f"📦 {pattern.name} ({pattern.provider.upper()})", expanded=(i==0)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {pattern.description}")
                    st.markdown(f"**Category:** {pattern.category.title()}")
                    st.markdown(f"**Files:** {', '.join(pattern.files) if pattern.files else 'Standard Terraform files'}")
                
                with col2:
                    st.markdown("**Details:**")
                    st.write(f"🏷️ Provider: {pattern.provider.upper()}")
                    st.write(f"📊 Level: {pattern.complexity.title()}")
                    
                    if st.button(f"📥 Download", key=f"download_{pattern.name}_{i}"):
                        # Get pattern code
                        pattern_files = fetcher.get_pattern_code(pattern)
                        
                        if pattern_files:
                            # Create ZIP
                            zip_data = create_terraform_zip(pattern_files)
                            
                            st.download_button(
                                label="📥 Download ZIP File",
                                data=zip_data,
                                file_name=f"{pattern.name.lower().replace(' ', '-')}.zip",
                                mime="application/zip",
                                key=f"download_zip_{pattern.name}_{i}"
                            )
                            
                            st.success(f"✅ Pattern '{pattern.name}' ready for download!")
                        else:
                            st.error("❌ Failed to generate pattern files")
    else:
        st.info("👆 Click 'Refresh Patterns' to load available templates")

def render_requirements_collector():
    """Render the requirements collection interface"""
    st.header("🤖 AI Terraform Code Generator")
    st.markdown("Describe your infrastructure needs and let AI generate production-ready Terraform code.")
    
    with st.form("terraform_requirements"):
        # Basic Information
        st.subheader("📋 Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            provider = st.selectbox(
                "Cloud Provider",
                ["AWS", "Azure", "GCP"],
                help="Select your target cloud provider"
            )
            
            environment = st.selectbox(
                "Environment",
                ["development", "staging", "production"],
                help="Target deployment environment"
            )
            
        with col2:
            region = st.text_input(
                "Primary Region", 
                value="us-west-2",
                help="Primary deployment region"
            )
            
            project_name = st.text_input(
                "Project Name",
                placeholder="my-terraform-project",
                help="Name for your infrastructure project"
            )
        
        # Services Selection
        st.subheader("🛠️ Required Services")
        
        if provider == "AWS":
            services = st.multiselect(
                "Select AWS Services",
                [
                    "EC2", "VPC", "S3", "RDS", "Lambda", 
                    "ELB", "CloudFront", "Route53", "EKS",
                    "ECS", "ElastiCache", "SQS", "SNS", "IAM"
                ],
                help="Choose the AWS services you need"
            )
        
        # Project Description
        st.subheader("📝 Project Description")
        description = st.text_area(
            "Describe your infrastructure requirements",
            placeholder="e.g., I need a scalable web application with load balancer, database, and CDN...",
            height=100,
            help="Provide detailed description of what you want to build"
        )
        
        # Configuration Options
        st.subheader("⚙️ Configuration Options")
        col3, col4 = st.columns(2)
        
        with col3:
            ha_required = st.checkbox("High Availability Required")
            backup_required = st.checkbox("Backup Strategy Required") 
            monitoring = st.checkbox("Include Monitoring")
        
        with col4:
            auto_scaling = st.checkbox("Auto Scaling Configuration")
            cost_optimization = st.checkbox("Cost Optimization")
            security_hardening = st.checkbox("Security Hardening", value=True)
        
        # Security & Compliance
        st.subheader("🔒 Security & Compliance")
        col5, col6 = st.columns(2)
        
        with col5:
            compliance = st.selectbox(
                "Compliance Requirements",
                ["Standard", "HIPAA", "SOC2", "PCI-DSS", "GDPR"]
            )
            
        with col6:
            vpc_config = st.selectbox(
                "VPC Configuration",
                ["Default", "Custom", "Multi-AZ", "Isolated"]
            )
        
        # Submit Button
        submitted = st.form_submit_button("🚀 Generate Terraform Code", type="primary")
        
        if submitted:
            # Validation
            if not project_name:
                st.error("❌ Project name is required!")
                return None
            
            if not services:
                st.error("❌ Please select at least one service!")
                return None
            
            if not description:
                st.error("❌ Project description is required!")
                return None
            
            # Build requirements dictionary
            requirements = {
                'provider': provider,
                'environment': environment,
                'region': region,
                'project_name': project_name,
                'services': services,
                'description': description,
                'compliance': compliance,
                'vpc_config': vpc_config,
                'ha_required': ha_required,
                'backup_required': backup_required,
                'monitoring': monitoring,
                'auto_scaling': auto_scaling,
                'cost_optimization': cost_optimization,
                'security_hardening': security_hardening
            }
            
            return requirements
    
    return None

def render_code_generator(generator, requirements):
    """Render code generation interface"""
    st.markdown("---")
    st.subheader("🎯 Generated Terraform Code")
    
    with st.spinner("🤖 AI is generating your Terraform code..."):
        try:
            generated_files = generator.generate_terraform_code(requirements)
            
            if generated_files:
                st.success("✅ Terraform code generated successfully!")
                
                # Display generated files in tabs
                file_tabs = st.tabs(list(generated_files.keys()))
                
                for tab, (filename, content) in zip(file_tabs, generated_files.items()):
                    with tab:
                        st.code(content, language='hcl', line_numbers=True)
                        
                        # Download button for individual files
                        st.download_button(
                            label=f"📥 Download {filename}",
                            data=content,
                            file_name=filename,
                            mime="text/plain",
                            key=f"download_{filename}"
                        )
                
                # Download all files as ZIP
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col2:
                    zip_data = create_terraform_zip(generated_files)
                    st.download_button(
                        label="📦 Download All Files (ZIP)",
                        data=zip_data,
                        file_name=f"{requirements['project_name']}-terraform.zip",
                        mime="application/zip",
                        type="primary"
                    )
                
                # Jenkins pipeline option
                render_jenkins_section(generated_files, requirements)
                
            else:
                st.error("❌ Failed to generate code. Please try again with different requirements.")
                
        except Exception as e:
            st.error(f"❌ Generation failed: {str(e)}")

def render_jenkins_section(files_dict, requirements):
    """Render Jenkins pipeline section"""
    st.markdown("---")
    st.subheader("🚀 CI/CD Pipeline Setup")
    
    with st.expander("Generate Jenkins Pipeline", expanded=False):
        st.markdown("Configure automated deployment pipeline for your Terraform code.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            jenkins_url = st.text_input("Jenkins URL", placeholder="https://jenkins.yourcompany.com")
            git_repo = st.text_input("Git Repository URL", placeholder="https://github.com/yourorg/terraform-repo")
        
        with col2:
            terraform_version = st.selectbox("Terraform Version", ["1.5.0", "1.4.0", "1.3.0"])
            auto_approve = st.checkbox("Auto-approve applies (⚠️ Use with caution)")
        
        if st.button("🔧 Generate Jenkins Pipeline"):
            pipeline_config = generate_jenkins_pipeline(
                requirements['project_name'],
                git_repo,
                terraform_version,
                auto_approve
            )
            
            st.code(pipeline_config, language='groovy')
            
            st.download_button(
                label="📥 Download Jenkinsfile",
                data=pipeline_config,
                file_name="Jenkinsfile",
                mime="text/plain"
            )

def render_analytics_dashboard():
    """Render analytics dashboard"""
    st.header("📊 Usage Analytics")
    st.markdown("Track usage patterns and system performance.")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Downloads", "1,247", delta="12%")
    with col2:
        st.metric("Code Generations", "856", delta="8%")
    with col3:
        st.metric("Success Rate", "94.2%", delta="2.1%")
    with col4:
        st.metric("Avg. Response Time", "3.4s", delta="-0.5s")
    
    # Sample charts using plotly (without pandas)
    st.markdown("---")
    
    # Usage over time
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Usage Trends")
        
        # Sample data using lists instead of pandas
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        pattern_downloads = [20, 25, 30, 35, 45, 50, 55, 60, 65, 70, 75, 80]
        ai_generations = [15, 20, 28, 35, 42, 48, 55, 62, 68, 75, 82, 90]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=pattern_downloads, mode='lines+markers', name='Pattern Downloads'))
        fig.add_trace(go.Scatter(x=months, y=ai_generations, mode='lines+markers', name='AI Generations'))
        fig.update_layout(title='Monthly Usage Trends', xaxis_title='Month', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏷️ Popular Categories")
        
        # Sample data
        categories = ['Compute', 'Storage', 'Networking', 'Database', 'Security']
        downloads = [120, 95, 110, 85, 70]
        
        fig = go.Figure(data=go.Pie(labels=categories, values=downloads))
        fig.update_layout(title='Downloads by Category')
        st.plotly_chart(fig, use_container_width=True)

def render_about_page():
    """Render about page"""
    st.header("ℹ️ About Terraform Code Generator")
    
    st.markdown("""
    ### 🎯 Purpose
    This application helps DevOps engineers and developers quickly generate production-ready 
    Terraform code using two powerful approaches:
    
    1. **Pattern Browser**: Download proven Terraform patterns from official repositories
    2. **AI Code Generator**: Generate custom code using Claude AI based on your requirements
    
    ### 🚀 Key Features
    - **Curated Patterns**: Access to proven Terraform modules
    - **AI-Powered Generation**: Custom code generation with best practices
    - **Multi-Cloud Support**: AWS, Azure, and GCP compatibility
    - **CI/CD Integration**: Automated Jenkins pipeline generation
    - **Security Focus**: Built-in compliance and security hardening
    
    ### 🛠️ Technology Stack
    - **Frontend**: Streamlit Cloud
    - **AI Engine**: Claude 3 Sonnet
    - **Pattern Source**: GitHub API
    - **Languages**: Python, HCL (Terraform)
    
    ### 📝 Getting Started
    1. Navigate to Pattern Browser to explore existing templates
    2. Use AI Code Generator to create custom infrastructure
    3. Download generated files and deploy with confidence
    
    ### 🔧 Configuration Required
    This app requires API keys to be configured in Streamlit Cloud:
    - `ANTHROPIC_API_KEY`: For AI code generation
    - `GITHUB_TOKEN`: For accessing GitHub repositories (optional)
    """)

# Main Application
def main():
    # Header
    st.markdown('<h1 class="main-header">🏗️ Terraform Code Generator</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=TerraGen", width=200)
        
        st.markdown("### 🚀 Navigation")
        module = st.radio(
            "Choose Module",
            ["🔍 Pattern Browser", "🤖 AI Code Generator", "📊 Analytics", "ℹ️ About"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        st.metric("Patterns Available", "50+", delta="5")
        st.metric("Code Generated", "1.2K+ files", delta="150")
        st.metric("Success Rate", "94.2%", delta="2.1%")
        
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown("- [Terraform Docs](https://terraform.io/docs)")
        st.markdown("- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws)")
        st.markdown("- [Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/)")
    
    # Check for API keys
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY")
    
    # Main content area
    if module == "🔍 Pattern Browser":
        render_pattern_browser()
        
    elif module == "🤖 AI Code Generator":
        if not anthropic_key:
            st.error("❌ Claude API key not configured!")
            st.info("Please add ANTHROPIC_API_KEY to your Streamlit Cloud secrets.")
            st.info("Get your API key from: https://console.anthropic.com/")
        else:
            claude_generator = ClaudeCodeGenerator(api_key=anthropic_key)
            requirements = render_requirements_collector()
            
            if requirements:
                render_code_generator(claude_generator, requirements)
                
    elif module == "📊 Analytics":
        render_analytics_dashboard()
        
    elif module == "ℹ️ About":
        render_about_page()

if __name__ == "__main__":
    main()