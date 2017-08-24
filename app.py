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
'''
# then run deploy
# then remove that code and run deploy --no-autogen-policy from then on

app = chalice.Chalice(app_name='awsplusplus')
app.debug = True
app.log.setLevel(logging.DEBUG)

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
