from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    Stack,
    CfnOutput
)
from constructs import Construct

class ECSService(Stack):

    def __init__(self, scope: Construct, id: str, vpc, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        starter_image = ecs.ContainerImage.from_registry("public.ecr.aws/b4f2s5k2/project-demo-reinvent/nginx-web-app:latest")
        execution_policy = iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name = "service-role/AmazonECSTaskExecutionRolePolicy")
        execution_role = iam.Role(
            self,
            "ecs-service-role-id", 
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[execution_policy],
            role_name="ecs-service-role")

        # fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,                
            task_image_options={
                'image': ecs.ContainerImage.from_registry("752783179453.dkr.ecr.eu-west-1.amazonaws.com/simple-api"),
                'execution_role' : execution_role
            }
        )

        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer = ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection = ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )

        CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )
        CfnOutput(
            self, "Service",
            value=fargate_service.service.service_name
        )