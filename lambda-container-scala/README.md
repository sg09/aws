# What this solution is trying to achieve?
Lambda cold start issues when using scala containers with AWS lambda

# Solutions flow

<img width="690" alt="image" src="https://user-images.githubusercontent.com/1725781/159613058-ab629463-3458-471f-9f23-2a756452dbe6.png">


# How this compared?

Two lambda functions are created with and without Provisioned Concurrency feature in AWS lambda:

<img width="1204" alt="image" src="https://user-images.githubusercontent.com/1725781/159613094-0cfd5bda-a1b8-4e8d-8f99-5adb8f1c12f2.png">


<img width="1203" alt="image" src="https://user-images.githubusercontent.com/1725781/159613134-b4806350-35dd-4d7f-9e04-ebb61ba37038.png">


<img width="1203" alt="image" src="https://user-images.githubusercontent.com/1725781/159613164-d5d22e1b-a58f-4307-a1fc-58a278162689.png">


# How to replicate this solution?

In the commands below, replace `<aws-region>` and `<aws-account-number>`.

Create ECR repository

```
aws ecr create-repository --region <aws-region> --repository-name lambda-scala
```

Login to ECR

```
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws-account-number>.dkr.ecr.<aws-region>.amazonaws.com
```

Build and tag the image

```
docker build . -t <aws-account-number>.dkr.ecr.<aws-region>.amazonaws.com/lambda-scala
```

Push the image

```
docker push <aws-account-number>.dkr.ecr.<aws-region>.amazonaws.com/lambda-scala
```

