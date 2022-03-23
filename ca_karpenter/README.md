# Cluster Autoscaling with Karpenter


## What is Karpenter?

* Open source, flexible, high-performance K8S CA built with AWS. 
* Rapidly launch right-sized compute resources in response to changing application loads. 
* Just-in-time compute resources to meet your application’s needs 
* Automatically optimize a cluster’s compute resource footprint to reduce costs and improve performance.


## Steps

### Prereq

```
export CLUSTER_NAME=$(eksctl get clusters -o json | jq -r '.[0].metadata.name')
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')

```

### Tag subnets with kubernetes.io/cluster/$CLUSTER_NAME


```
SUBNET_IDS=$(aws cloudformation describe-stacks --stack-name eksctl-${CLUSTER_NAME}-cluster --query 'Stacks[].Outputs[?OutputKey==`SubnetsPrivate`].OutputValue' --output text)
aws ec2 create-tags  --resources $(echo $SUBNET_IDS | tr ',' '\n’)  --tags Key="kubernetes.io/cluster/${CLUSTER_NAME}",Value=

```


### IAM role and instance profile creation for Karpenter nodes

```
TEMPOUT=$(mktemp)
curl -fsSL https://karpenter.sh/v0.6.4/docs/getting-started/cloudformation.yaml > $TEMPOUT && aws cloudformation deploy --stack-name Karpenter-${CLUSTER_NAME} --template-file ${TEMPOUT} --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ClusterName=${CLUSTER_NAME}

```


### Grant access to nodes using profile to connect to cluster

```
eksctl create iamidentitymapping --username system:node:{{EC2PrivateDNSName}} --cluster  ${CLUSTER_NAME} --arn arn:aws:iam::${ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME} --group system:bootstrappers  --group system:nodes

```


### Create Karpenter Controller IAM role

```
eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} --approve
```


### Create IAM role for Service account

```
eksctl create iamserviceaccount  --cluster $CLUSTER_NAME --name karpenter --namespace karpenter --attach-policy-arn arn:aws:iam::$ACCOUNT_ID:policy/KarpenterControllerPolicy-$CLUSTER_NAME --approve

```


### Install Karpenter with helm

```
helm repo add karpenter https://charts.karpenter.sh; helm repo update
helm upgrade --install karpenter karpenter/karpenter --namespace karpenter --create-namespace --set serviceAccount.create=false --version 0.4.3 --set controller.clusterName=${CLUSTER_NAME} --set controller.clusterEndpoint=$(aws eks describe-cluster --name ${CLUSTER_NAME} --query "cluster.endpoint" --output json) --set defaultProvisioner.create=false
```


### Setup provisioner

Sample below


<img width="465" alt="image" src="https://user-images.githubusercontent.com/1725781/159614738-08cbb18a-bd70-4fc7-92e2-8c5885911a7a.png">


### Deploy some pods
```
cat << EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testCA
spec:
  replicas: 0
  selector:
    matchLabels:
      app: testCA
  template:
    metadata:
      labels:
        app: testCA
    spec:
      nodeSelector:
        intent: apps
      containers:
        - name: testCA
          image: public.ecr.aws/eks-distro/kubernetes/pause:3.2
          resources:
            requests:
              cpu: 1
              memory: 1.5Gi
EOF

kubectl apply -f deploy.yaml

```


### Test cluster autoscaler
```
//scale Up
kubectl scale deployment testCA --replicas=1
kubectl scale deployment testCA --replicas=1

//scale down
kubectl scale deployment testCA --replicas=0
```


> For every invocation of above command, try to see nodes by specifying "kubectl get nodes" and the type of EC2 instances created
>
>> Also karpenter logs provide much information on this as well.
