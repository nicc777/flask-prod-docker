terraform {
  backend "s3" {
    bucket = "terraform-state-k0ioo07m"
    encrypt = true
    key    = "poc/flask-prod-docker/terraform.tfstate"
    dynamodb_table = "terraform_state"
    region = "us-east-1"
  }
}