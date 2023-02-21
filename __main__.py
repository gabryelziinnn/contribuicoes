import pulumi, hashlib, json
import pulumi_aws as aws

iam_for_lambda = aws.iam.Role("iamForLambda", assume_role_policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
""")

projeto = aws.lambda_.Function("projeto-ssl",
    # Insira aqui o nome da bucket
    s3_bucket=
    # Insira o caminho para a mesma
    s3_key=
    role=iam_for_lambda.arn,
    description='Funcao para realizar a verificacao dos certificados SSL',
    runtime="python3.9",
    handler="lambda_function.lambda_handler",
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            INSIRA SEUS DADOS AQUI DO WEBHOOK E SENHA DE EMAIL
        },
    ))

# Define a CloudWatch Event Rule to trigger the Lambda function
cloud_watch_rule = aws.cloudwatch.EventRule("trigger-lambda",
    name='lambda-trigger-ssl-project',
    description='Trigger em minha funcao lambda',
    schedule_expression="cron(0 12 * * ? *)"
    )

# Define the target for the CloudWatch Event Rule
target = aws.cloudwatch.EventTarget("target",
    rule=cloud_watch_rule.name,
    arn=projeto.arn,
    target_id="meu-projeto-lamda"
    )



# Invoca a funcao
# invocacao = aws.lambda_.Invocation("invocar",
#     function_name=projeto.name,
#     input=json.dumps({})
#     )

pulumi.export("rule_name", cloud_watch_rule.name)
pulumi.export("function_arn", projeto.arn)