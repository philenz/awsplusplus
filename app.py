import chalice
import chalicelib.ec2
import logging

app = chalice.Chalice(app_name='awsplusplus')
app.debug = True
app.log.setLevel(logging.DEBUG)

# Need to raise bug...
# Policy generator doesn't scan code in chalicelib
# so need to add these here...
#import boto3
#sgs = boto3.client('ec2', region_name='ap-southeast-2').describe_security_groups()
#reservations = boto3.client('ec2', region_name='ap-southeast-2').describe_instances()
# then run deploy
# then remove that code and run deploy --no-autogen-policy from then on

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
