#!/usr/bin/env python3
import boto3
import traceback
import random
import argparse
import sys
import os


def generate_s3_bucket_name(base_name: str='terraform-state-')->str:
    bucket_name = base_name
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_bit = ''
    while len(random_bit) < 8:
        random_bit = '{}{}'.format(
            random_bit,
            random.choice(chars)
        )
    bucket_name = '{}{}'.format(bucket_name, random_bit)
    return bucket_name


parser = argparse.ArgumentParser(description='Prepare the AWS components for the Terraform backend')
parser.add_argument(
    '--s3',
    metavar='NAME',
    type=str,
    help='The name of the S3 bucket to use.',
    default=generate_s3_bucket_name()
)
parser.add_argument(
    '--dynamodb',
    metavar='NAME',
    type=str,
    help='The name of the DynamoDB table to use.',
    default='terraform_state'
)
args = parser.parse_args()


def get_all_iam_policies(marker: str=None)->list:
    result = list()
    try:
        client = boto3.client('iam')
        new_marker = None
        if marker is None:
            response = client.list_policies(
                Scope='Local',
                OnlyAttached=False,
                PolicyUsageFilter='PermissionsPolicy',
                MaxItems=100
            )
            if 'Policies' in response:
                for policy in response['Policies']:
                    if 'PolicyName' in policy:
                        result.append(policy['PolicyName'])
            if 'Marker' in response:
                new_marker = response['Marker']
        else:
            response = client.list_policies(
                Scope='Local',
                OnlyAttached=False,
                PolicyUsageFilter='PermissionsPolicy',
                Marker=marker,
                MaxItems=100
            )
            if 'Policies' in response:
                for policy in response['Policies']:
                    if 'PolicyName' in policy:
                        result.append(policy['PolicyName'])
            if 'Marker' in response:
                new_marker = response['Marker']  
        if new_marker is not None:
            result += get_all_iam_policies(marker=new_marker)   
    except:
        traceback.print_exc()
    print('info: retrieved {} custom policy definitions'.format(len(result)))
    return result


def check_policy(policy_name: str='terraform-backend-policy')->bool:
    print('info: checking if policy name "{}" exist'.format(policy_name))
    if policy_name in get_all_iam_policies():
        return True
    return False


def load_policy_file(file_name: str='backend_policy.json')->str:
    data = None
    try:
        with open(file_name) as f:
            data = f.read()
    except:
        traceback.print_exc()
    if data is None:
        raise Exception('Could not load policy data')
    return data


def create_policy(
    bucket_name: str,
    dynamodb_table_name: str,
    policy_name: str='terraform-backend-policy',
    local_policy_filename: str='backend_policy.json'
)->bool:
    print('info: creating policy "{}"'.format(policy_name))
    policy_text = load_policy_file(file_name=local_policy_filename)
    policy_text = policy_text.replace('__STATE_BUCKET_NAME__', bucket_name)
    policy_text = policy_text.replace('__DYNAMODB_TABLE_NAME__', dynamodb_table_name)
    try:
        client = boto3.client('iam')
        response = client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=policy_text,
            Description='A policy to enable Terraform to use AWS as a backend.'
        )
        if 'Policy' in response:
            if 'Arn' in response['Policy']:
                print('info: created policy with ARN "{}"'.format(response['Policy']['Arn']))
            else:
                print('warning: could not determine ARN - something may have gone wrong!')
        else:
            print('warning: it does not appear that the policy was created.')
    except:
        traceback.print_exc()
    return check_policy(policy_name=policy_name)


def get_all_s3_buckets()->list:
    buckets = list()
    try:
        client = boto3.client('s3')
        response = client.list_buckets()
        if 'Buckets' in response:
            for bucket in response['Buckets']:
                buckets.append(bucket['Name'])
    except:
        traceback.print_exc()
    print('info: retrieved {} buckets'.format(len(buckets)))
    return buckets


def create_s3_bucket(s3_bucket_name: str)->bool:
    result = False
    try:
        if s3_bucket_name not in get_all_s3_buckets():
            client = boto3.client('s3')
            response = client.create_bucket(
                ACL='private',
                Bucket=s3_bucket_name
            )
            if 'Location' in response:
                print('info: s3 location: {}'.format(response['Location']))
                if s3_bucket_name in get_all_s3_buckets():
                    result = True
        else:
            print('info: s3 bucket "{}" already exists'.format(s3_bucket_name))
            result = True
    except:
        traceback.print_exc()
    return result


def get_all_dynamodb_tables(start_table_name: str=None)->list:
    tables = list()
    try:
        client = boto3.client('dynamodb')
        if start_table_name is not None:
            response = client.list_tables(
                ExclusiveStartTableName=start_table_name,
                Limit=100
            )
            start_table_name = None
            if 'TableNames' in response:
                for table_name in response['TableNames']:
                    tables.append(table_name)
            
            if 'LastEvaluatedTableName' in response:
                if response['LastEvaluatedTableName'] is not None:
                    start_table_name = response['LastEvaluatedTableName']
        else:
            response = client.list_tables(Limit=100)
            start_table_name = None
            if 'TableNames' in response:
                for table_name in response['TableNames']:
                    tables.append(table_name)
            
            if 'LastEvaluatedTableName' in response:
                if response['LastEvaluatedTableName'] is not None:
                    start_table_name = response['LastEvaluatedTableName']
        if start_table_name is not None:
            tables += get_all_dynamodb_tables(start_table_name=start_table_name)
    except:
        traceback.print_exc()
    print('info: retrieved {} tables'.format(len(tables)))
    return tables


def create_dynamodb_table(table_name: str)->bool:
    result = False
    try:
        if table_name not in get_all_dynamodb_tables():
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'LockID',
                        'AttributeType': 'S'
                    },
                ],
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'LockID',
                        'KeyType': 'HASH'
                    },
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        if table_name in get_all_dynamodb_tables():
            result = True
            print('info: DynamoDB table "{}" created'.format(table_name))
    except:
        traceback.print_exc()
    return result


def setup_backend_file(
    s3_bucket_name: str,
    dynamodb_table_name: str,
    filename: str='terraform/backend.tf',
    template: str='terraform/backend.TENPLATE',
)->bool:
    result = False
    try:
        backend_content = ''
        with open(template) as f:
            backend_content = f.read()
        backend_content = backend_content.replace('__STATE_BUCKET_NAME__', s3_bucket_name)
        backend_content = backend_content.replace('__DYNAMODB_TABLE_NAME__', dynamodb_table_name)
        if os.path.exists(filename):
            print('info: removing previous file: "{}"'.format(filename))
            os.unlink(filename)
        with open(filename, 'w') as f:
            f.write(backend_content)
        if os.path.exists(filename):
            result = True
            print('info: created "{}'.format(filename))
    except:
        traceback.print_exc()
    return result


if __name__ == '__main__':
    print('START')
    bucket_name = args.s3
    dynamodb_table_name = args.dynamodb
    print('info: bucket_name={}'.format(bucket_name))
    print('info: dynamodb_table_name={}'.format(dynamodb_table_name))
    print('info: S3 bucket name set to "{}"'.format(bucket_name))
    if check_policy() is False:
        if create_policy(bucket_name=bucket_name, dynamodb_table_name=dynamodb_table_name) is False:
            print('critical: failed to create a policy. quiting.')
            sys.exit(-1)
    if create_s3_bucket(s3_bucket_name=bucket_name) is False:
        print('critical: failed to create a s3 bucket. quiting.')
        sys.exit(-1)
    if create_dynamodb_table(table_name=dynamodb_table_name) is False:
        print('critical: failed to create a DynamoDB table. quiting.')
        sys.exit(-1)
    if setup_backend_file(
        s3_bucket_name=bucket_name,
        dynamodb_table_name=dynamodb_table_name,
        filename='terraform/backend.tf',
        template='terraform/backend.TEMPLATE'
    ) is False:
        print('critical: failed to create a Terraform backend file. quiting.')
        sys.exit(-1)
    print('DONE')
