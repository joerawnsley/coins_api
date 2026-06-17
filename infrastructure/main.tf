provider "aws" {
  region = "eu-west-2"
}

# AWS ECR REPOSITORY
resource "aws_ecr_repository" "app_repo" {
  name                 = "jbr-coins-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


# Define the Trust Policy
data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::261219435789:oidc-provider/token.actions.githubusercontent.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:joerawnsley/coins_api:*"]
    }
  }
}

# Create IAM Role
resource "aws_iam_role" "github_actions_ecr_role" {
  name               = "github-actions-ecr-push-jbr"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json
}

# Attach policy to the role
resource "aws_iam_role_policy_attachment" "attach_ecr_power_user" {
  role       = aws_iam_role.github_actions_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

# outputs
output "ecr_repository_url" {
  value       = aws_ecr_repository.app_repo.repository_url
  description = "ECR repository URL"
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions_ecr_role.arn
  description = "ARN of the IAM role for GitHub Actions to assume."
}