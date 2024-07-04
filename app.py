
import aws_cdk as cdk
import json
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_elasticloadbalancingv2 as elb,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets,
)
class TestStack(Stack):
 
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        security_group_id = config.get('securityGroupId')
        alb_securityGroupId = config.get('alb_securityGroupId')
        vpc_id = config.get('vpc_id')
        availability_zones = config.get('availability_zones')
        public_subnet_ids = config.get('public_subnet_ids')
        private_subnet_ids = config.get('private_subnet_ids')
        role_arn = config.get('role_arn')
        region = config.get('region')
        ami_id = self.node.try_get_context("ami_id")
        az_1 = self.node.try_get_context("site_1")
        az_2 = self.node.try_get_context("site_2")
        target_group_name = config.get('test_target_group')
        ssl_certificate_arn = config.get('ssl_certificate_arn')
        InstanceType = config.get('instance_type')
       
        vpc = ec2.Vpc.from_vpc_attributes(
            self, 'ImportedVpc',
            vpc_id= vpc_id,
            availability_zones=availability_zones,  
            public_subnet_ids=public_subnet_ids, 
            private_subnet_ids = private_subnet_ids, 
        )

        role = iam.Role.from_role_arn(
            self, "ExistingRole", role_arn=role_arn
        )


        existing_security_group = ec2.SecurityGroup.from_security_group_id(
            self, 'ImportedSecurityGroup',
            security_group_id=security_group_id,
        )

        alb_sg = ec2.SecurityGroup.from_security_group_id(
            self, 'ImportedALBSecurityGroup',
            security_group_id=alb_securityGroupId,
        )

        ec2_instance = ec2.Instance(
            self,
            "WA-Prod-build_site-1",
            instance_type=ec2.InstanceType(InstanceType),
            machine_image=ec2.MachineImage.generic_linux(ami_map={region: ami_id}),
            vpc=vpc,
            security_group=existing_security_group,
            role= role,
            availability_zone=az_1,
        )
        ec2_instance.instance.add_property_override("DisableApiTermination",True)
        
        ec2_instance1 = ec2.Instance(
            self,"WA-Prod-build_site-2",
            instance_type=ec2.InstanceType(InstanceType),
            machine_image=ec2.MachineImage.generic_linux(ami_map={region: ami_id}),
            vpc=vpc,
            security_group=existing_security_group,
            role= role,
            availability_zone=az_2   
        )
        ec2_instance1.instance.add_property_override("DisableApiTermination",True)

        ec2_instance.apply_removal_policy(cdk.RemovalPolicy.RETAIN)
        ec2_instance1.apply_removal_policy(cdk.RemovalPolicy.RETAIN)

        alb = elb.ApplicationLoadBalancer(self, "MyALB",
            vpc=vpc,
            security_group=alb_sg,
            internet_facing=True  # Set to False if internal facing
        )
                
        target_group = elb.ApplicationTargetGroup(
            self, target_group_name,
            port=443,  # Set the desired port
            vpc=vpc,
            health_check=elb.HealthCheck(path="/TWA/health", port="443",healthy_http_codes="200-499"),  # Customize health check settings as needed
        )

        instance_target = elasticloadbalancingv2_targets.InstanceTarget(ec2_instance, 443)
        instance_target1 = elasticloadbalancingv2_targets.InstanceTarget(ec2_instance1, 443)
        target_group.add_target(instance_target)
        target_group.add_target(instance_target1)
        alb.add_listener('MyNewListener',
            port=443,  # Set the desired listener port
            certificates= [elb.ListenerCertificate.from_arn(ssl_certificate_arn)],
            default_target_groups=[target_group],
        )
        ssm.StringParameter(self, "InstanceIdParameter",
            parameter_name="ec2instance1",
            string_value=ec2_instance.instance_id
        )
        ssm.StringParameter(self, "InstanceIdParameter1",
            parameter_name="ec2instance2",
            string_value=ec2_instance1.instance_id
        )

        ssm.StringParameter(self, "ALBNameParameter",
            parameter_name="test_alb_name",
            string_value=alb.load_balancer_name
        )

        # Store ALB DNS name in SSM Parameter Store
        ssm.StringParameter(self, "ALBDNSParameter",
            parameter_name="test_alb_dns",
            string_value=alb.load_balancer_dns_name
        )


class ProdStack(Stack):
 
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        security_group_id = config.get('prod_alb_securityGroupId')
        vpc_id = config.get('vpc_id')
        availability_zones = config.get('availability_zones')
        public_subnet_ids = config.get('public_subnet_ids')
        prod_alb_arn = config.get('prod_alb_arn')
        target_group_name = config.get('prod_target_group')
        instance1 = ssm.StringParameter.from_string_parameter_attributes(self, "MyValue",parameter_name="ec2instance1").string_value
        instance2 = ssm.StringParameter.from_string_parameter_attributes(self, "MyValue1",parameter_name="ec2instance2").string_value
        ssl_certificate_arn = config.get('ssl_certificate_arn')

        vpc = ec2.Vpc.from_vpc_attributes(
            self, 'ImportedVpc',
            vpc_id= vpc_id,
            availability_zones=availability_zones,  
            public_subnet_ids=public_subnet_ids,  
        )

        alb = elb.ApplicationLoadBalancer.from_application_load_balancer_attributes(
            self, 'ImportedALB',
            load_balancer_arn=prod_alb_arn,
            security_group_id=security_group_id
        )
                
        target_group = elb.ApplicationTargetGroup(
            self, target_group_name,
            port=443,  # Set the desired port
            vpc=vpc,
            health_check=elb.HealthCheck(path="/TWA/health", port="443",healthy_http_codes="200-499"),  # Customize health check settings as needed
        )

        instance_target = elasticloadbalancingv2_targets.InstanceIdTarget(instance1, 443)
        instance_target1 = elasticloadbalancingv2_targets.InstanceIdTarget(instance2, 443)
        target_group.add_target(instance_target)
        target_group.add_target(instance_target1)
        alb.add_listener('MyNewListener',
            port=443,  # Set the desired listener port
            certificates= [elb.ListenerCertificate.from_arn(ssl_certificate_arn)],
            default_target_groups=[target_group],
        )




with open('config.json', 'r') as config_file:
    config = json.load(config_file)
env = cdk.Environment(account=config.get('account_id'), region=config.get('region'))
app = cdk.App()
TestStack(app, "TestStack" ,env=env) 
ProdStack(app, "ProdStack" ,env=env)
app.synth()



