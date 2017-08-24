import boto3

from collections import namedtuple
from datetime import datetime

def key_age(key_created_date):
    tz_info = key_created_date.tzinfo
    age = datetime.now(tz_info) - key_created_date

    key_age_str = str(age)
    if 'days' not in key_age_str:
        return 0

    days = int(key_age_str.split(',')[0].split(' ')[0])

    return days


# Return a list of users

Users = namedtuple(
    'Users', ['users'])

class UserList():
        def get_users(self):

            client = boto3.client('iam')

            userList = client.list_users()

            users = []
            for u in userList['Users']:

                user = { 'id': u['UserId'] }
                user['name'] = u['UserName']

                users.append(user)

            return Users(
                users=users
            )


# Return a user's access keys

Keys = namedtuple(
    'Keys', ['keys'])

class AccessKeys():
    def get_access_keys(self, user_name):

        client = boto3.client('iam')
        accessKeys = client.list_access_keys(UserName=user_name)['AccessKeyMetadata']

        keys = []

        for ak in accessKeys:
            key = {'id': ak['AccessKeyId']}
            key['status'] = ak['Status']
            key['age'] = key_age(ak['CreateDate'])

            keys.append(key)

        return Keys(
            keys=keys
        )
