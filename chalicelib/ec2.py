import boto3

from collections import namedtuple


# Return a list of instance ids

Instances = namedtuple(
    'Instances', ['instances'])

class InstanceList():
        def get_instances(self):

            client = boto3.client('ec2', region_name='ap-southeast-2')

            reservations = client.describe_instances()

            # Add filters like this...
            '''
            Filters=[
                    {
                        'Name': 'tag:ShutdownAfterHours',
                        'Values': ['True']
                    }
                ]   
            )
            '''

            instances = []
            for reservation in reservations['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance['InstanceId'])

            return Instances(
                instances=instances
            )
