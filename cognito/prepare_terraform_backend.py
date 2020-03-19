#!/usr/bin/env python3
import boto3
import traceback
import random


def generate_s3_bucket_name(base_name: str='terraform-state-')->str:
    bucket_name = base_name
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    random_bit = ''
    while len(random_bit) < 8:
        random_bit = '{}{}'.format(
            random_bit,
            random.choice(chars)
        )
    bucket_name = '{}{}'.format(bucket_name, random_bit)
    return bucket_name


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


def create_policy(
    bucket_name: str,
    dynamodb_table_name: str,
    policy_name: str='terraform-backend-policy'
)->bool:
    print('info: creating policy "{}"'.format(policy_name))
    try:
        # client = boto3.client('iam')
        # response = client.create_policy(
        #     PolicyName=policy_name,
        #     PolicyDocument='string',
        #     Description='A policy to enable Terraform to use AWS as a backend.'
        # )
        # if 'Policy' in response:
        #     if 'Arn' in response['Policy']:
        #         print('info: created policy with ARN "{}"'.format(response['Policy']['Arn']))
        #     else:
        #         print('warning: could not determine ARN - something may have gone wrong!')
        # else:
        #     print('warning: it does not appear that the policy was created.')
        pass
    except:
        traceback.print_exc()
    return check_policy(policy_name=policy_name)



if __name__ == '__main__':
    print('START')
    bucket_name = generate_s3_bucket_name()
    dynamodb_table_name = 'terraform_state'
    print('info: S3 bucket name set to "{}"'.format(bucket_name))
    if check_policy() is False:
        if create_policy(bucket_name=bucket_name, dynamodb_table_name=dynamodb_table_name) is False:
            print('critical: failed to create a policy. quiting.')
        else:
            pass
    print('DONE')
