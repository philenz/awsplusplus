import boto3

from collections import namedtuple

# Return a list of instance ids

Instances = namedtuple(
    'Instances', ['instances'])

class InstanceList():
        def get_instances(self):

            client = boto3.client('ec2', region_name='ap-southeast-2')

            reservations = client.describe_instances()

            instances = []
            for reservation in reservations['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance['InstanceId'])

            return Instances(
                instances=instances
            )

# Return a list of security group ids

SecurityGroups = namedtuple(
    'SecurityGroups', ['security_groups'])

class SecurityGroupList():
        def get_security_groups(self):

            client = boto3.client('ec2', region_name='ap-southeast-2')

            sgs = client.describe_security_groups()

            security_groups = []
            for sg in sgs['SecurityGroups']:
                security_groups.append(sg['GroupId'])

            return SecurityGroups(
                security_groups=security_groups
            )

# Return security group details

SecurityGroup = namedtuple(
    'SecurityGroup', ['id', 'name', 'vpc', 'description'])

class SecurityGroupId():
        def get_security_group(self, id):

            client = boto3.client('ec2', region_name='ap-southeast-2')
            sgs = client.describe_security_groups(
                GroupIds=[id]
            )

            sg = sgs['SecurityGroups'][0]

            return SecurityGroup(
                id=id,
                name=sg['GroupName'],
                vpc=sg['VpcId'],
                description=sg['Description']
            )
