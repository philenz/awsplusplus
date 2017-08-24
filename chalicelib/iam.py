import boto3

from collections import namedtuple


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
