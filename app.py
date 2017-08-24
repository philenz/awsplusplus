import chalice
import chalicelib.ec2
import chalicelib.iam
import logging

# Need to raise bug...
# Policy generator doesn't scan code in chalicelib
# so need to add these here...
'''
import boto3
sgs = boto3.client('ec2', region_name='ap-southeast-2').describe_security_groups()
reservations = boto3.client('ec2', region_name='ap-southeast-2').describe_instances()
users = boto3.client('iam').list_users()
keys = boto3.client('iam').list_access_keys(UserName='phil.evans@gallagher.com')['AccessKeyMetadata']
'''
# then run deploy
# then remove that code and run deploy --no-autogen-policy from then on

app = chalice.Chalice(app_name='awsplusplus')
app.debug = True
app.log.setLevel(logging.INFO)



@app.route('/', cors=True)
def index():
    return { 'AWS++': 'https://github.com/philenz/awsplusplus' }

@app.route('/instances', cors=True)
def list_instances():
    instanceList = chalicelib.ec2.InstanceList()
    instances = instanceList.get_instances()

    for instance in instances.instances:
        app.log.debug(instance)

    return {
        'instances': instances.instances
    }

@app.route('/securitygroups', cors=True)
def list_security_groups():
    sgList = chalicelib.ec2.SecurityGroupList()
    sgs = sgList.get_security_groups()

    for sg in sgs.security_groups:
        app.log.debug(sg)

    return {
        'security_groups': sgs.security_groups
    }

@app.route('/securitygroup/{security_group_id}', cors=True)
def get_security_group(security_group_id):
    sgId = chalicelib.ec2.SecurityGroupId()
    sg = sgId.get_security_group(security_group_id)
    if not sg:
        raise chalice.NotFoundError('Security Group does not exist')
    return {
        'id': sg.id,
        'name': sg.name,
        'vpc': sg.vpc,
        'description': sg.description
    }

@app.route('/users', cors=True)
def list_users():
    uList = chalicelib.iam.UserList()
    users = uList.get_users()

    for user in users.users:
        app.log.debug(user)

    return {
        'users': users.users
    }

@app.route('/accesskeys/{user_name}', cors=True)
def get_access_keys(user_name):

    app.log.info("get_access_keys for " + user_name)

    keyList = chalicelib.iam.AccessKeys()
    keys = keyList.get_access_keys(user_name)

    for key in keys.keys:
        app.log.info(key)

    return {
        'keys': keys.keys
    }

@app.route('/userskeys', cors=True)
def list_users_keys():
    uList = chalicelib.iam.UserKeyList()
    users = uList.get_users_plus_keys()

    for user in users.users_keys:
        app.log.debug(user)

    return {
        'userskeys': users.users_keys
    }
