# Cognito Terraform Setup

This section of the project contains Terraform and related scripts to get a Cognito environment set-up.

## Preparation

This solution assumes you are storing your Terraform state in AWS S3 and DynamoDB. This section quickly explains what you need to do to set this up.

__IMPORTANT__ In the `terraform/backend.tf` file, you need to set a different S3 bucket name than the one supplied. S3 bucket names have to be globally unique. The one in the file is just an example, but there's a good change someone will use it - and it's a first-come-first-serve kinda thing.

You can either modify the `terraform/backend.tf` file yourself to suite your needs, or continue through this section to run the preparation script that will setup your AWS backend.

Assuming all the requirements (see root [README](../README.md)) are met, you can run the following, assuming you are in the base directory of the project:

_Note_: You may need to set your AWS credentials. The first two commands is for setting your AWS administrative credentials.

```
(venv) $ export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxx
(venv) $ export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxx
(venv) $ cd cognito
(venv) $ ./prepare_terraform_backend.py 
```

## Usage

`TODO`
