import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_101_in_python.aws_cdk_101_in_python_stack import AwsCdk101InPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_101_in_python/aws_cdk_101_in_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdk101InPythonStack(app, "aws-cdk-101-in-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
