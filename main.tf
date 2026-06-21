terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws" 
  version = "~> 5.8"  
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true  
  
  tags = {
    Terraform = "true"
    Environment = "dev"
  }
  
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"  
  
  
  cluster_name    = "my-cluster"
  cluster_version = "1.30"
  
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    eks-pod-identity-agent = {
      most_recent = true
    }
  }
  
  cluster_endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]  
      min_size       = 1
      max_size       = 3
      desired_size   = 2
   
    }
  }
  
  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}
