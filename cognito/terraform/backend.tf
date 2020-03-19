terraform {
  backend "s3" {
    bucket = "__STATE_BUCKET_NAME__"
    encrypt = true
    key    = "poc/flask-prod-docker/terraform.tfstate"
    dynamodb_table = "terraform_state_table"
    region = "eu-west-2"
  }
}