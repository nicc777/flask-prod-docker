# A demo user pool
resource "aws_cognito_user_pool" "demo_pool" {
  name = "demo-pool"
  tags = {
    Name = "cognito-demo-pool"
    Project = "Wakanda"
    SubProject = "ApiGwDemo"
    Terraform = "TRUE"
  }
}

# User pool domain
resource "aws_cognito_user_pool_domain" "demo_pool_domain" {
  domain       = "${var.COGNITO_DOMAIN_NAME}"
  user_pool_id = "${aws_cognito_user_pool.demo_pool.id}"
}

# App 1
resource "aws_cognito_user_pool_client" "client_app_1" {
  name = "app1"
  user_pool_id = "${aws_cognito_user_pool.demo_pool.id}"
  generate_secret = true
  callback_urls = ["http://localhost:8080/cognito_callback"]
  logout_urls = ["http://localhost:8080/cognito_logout_callback"]
  allowed_oauth_flows = ["code"]
  allowed_oauth_scopes = ["openid", "profile", "email"]
  allowed_oauth_flows_user_pool_client = true
}

# OUTPUTS
output "app_1_id" {
    value = aws_cognito_user_pool_client.client_app_1.id
}

output "app_1_secret" {
    value = aws_cognito_user_pool_client.client_app_1.client_secret
}

output "user_pool_endpoint" {
    value = aws_cognito_user_pool.demo_pool.endpoint
}

output "user_pool_id" {
    value = aws_cognito_user_pool.demo_pool.id
}

output "user_pool_arn" {
    value = aws_cognito_user_pool.demo_pool.arn
}

output "user_pool_domain_name" {
    value = join("", ["https://", "${var.COGNITO_DOMAIN_NAME}", ".auth.eu-west-2.amazoncognito.com"])
}