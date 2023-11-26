from aws_cdk import (
    Stack, CfnOutput, Duration, RemovalPolicy,
    aws_ec2 as ec2,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment
)
from constructs import Construct

class AwsCdk101InPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        USER_NAME = "wyne"

        # ====================== Example 1 ======================
        # Select the default vpc
        vpc = ec2.Vpc.from_lookup(self, "default-vpc", is_default=True)

        # Create a security group
        awsug_sg_http = ec2.SecurityGroup(self, f"awsug-sg-http-{USER_NAME}",
            vpc=vpc,
            description="Allow traffic access through HTTP",
            allow_all_outbound=True
        )

        # Add an ingress rule to allow HTTP traffic from anywhere
        awsug_sg_http.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80), 
            "Allow http access from the world"
        )

        # Create an EC2 instance
        awsug_ec2 = ec2.Instance(self, f"awsug-ec2-{USER_NAME}",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.T3,
                instance_size=ec2.InstanceSize.MICRO
            ),
            security_group=awsug_sg_http,
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
        )

        # Print out the EC2 public IP address
        CfnOutput(self, "EC2 Public DNS Name", value=awsug_ec2.instance_public_dns_name)

        # ====================== Example 2 ======================
        # Create a role for Lambda
        awsug_lambda_role = iam.Role(
            self,"awsug_lambda_role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            )
        )

        # Create a Lambda Function
        awsug_lambda = lambda_.Function(
            self, "awsug_lambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("src"),
            handler="lambda_function.lambda_handler",
            role=awsug_lambda_role,
            timeout=Duration.seconds(30)
        )

        # Create an API Gateway
        awsug_apigw = apigw.RestApi(
            self, "awsug_apigw",
            rest_api_name="awsug_apigw",
            description="The AWS User Group Meetup Demo Use"
        )

        # Create two path(one with resource and the other is root) for the API Gateway
        awsug_apigw.root.add_method("GET", apigw.LambdaIntegration(awsug_lambda))
        awsug_apigw.root.add_resource("awsug").add_method("GET", apigw.LambdaIntegration(awsug_lambda))

        # Print out the API Gateway URL
        CfnOutput(self, "API Gateway URL", value=awsug_apigw.url)

        # ====================== Example 3 ======================
        # Create a bucket
        awsug_s3_bucket = s3.Bucket(
            self, "awsug_s3_bucket",
            bucket_name=f"awsug-s3-bucket-{USER_NAME}"
        )

        # Create a static web hosting for the bucket
        s3_deployment.BucketDeployment(
            self, "awsug_s3_bucket_deployment",
            destination_bucket=awsug_s3_bucket,
            sources=[s3_deployment.Source.asset("static_web_hosting")]
        )

        # Print out the S3 Bucket URL
        CfnOutput(self, "S3 Bucket URL", value=awsug_s3_bucket.bucket_website_url)