
# CDK Fargate Example

This example will deploy an ECS Fargate service with an ALB running a simple node application using the CDK. 

To run:
```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt 

cdk deploy --all
(y/n)? y 
```

To tear down the stacks
```
cdk destroy --all 
```
