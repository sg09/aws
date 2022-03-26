# Managing Amazon EKS control plane events


## Context
Currently EKS event TTL is set to 60m. Some customers have shown interest to increase the TTL. (https://github.com/aws/containers-roadmap/issues/785). It will be an additional burden if EKS control plane provided the option to increase TTL as this will add load to ETCD and storage. This solution here tries to bridge the gap to capture events beyond 60 minutes to cloudwatch, if the customers still achieve the same. That way control plane event TTL is not modified but at the sametime, if customer wanted to capture the events beyond 60m, they could achieve the same.


## Prerequisites

For this walkthrough, you should have the following prerequisites: 

* An AWS account 
* Running AWS EKS cluster 
* Basic Kubernetes knowledge (Pods, namespace and deployments)

## Solution flow

<img width="639" alt="image" src="https://user-images.githubusercontent.com/1725781/159606567-abc3273c-2803-40a3-ac3b-dd4bbbd67334.png">



## Files

| Directory     | Contents    |Target|
| ------------- |:-------------:|:--------:|
| app          | Files for containerization     |ECR|
| k8_utils      | Files for EKS data planes  |EKS |

### Files inside app

| File     | Contents     |
| ------------- |:-------------:|
| Dockerfile          | File for containerization     |
| requirements.txt      | Python dependency |
| event_loop.py | Control plane event blueprint|


### Files inside k8_utils

| File     | Contents     |
| ------------- |:-------------:|
| deployment.yaml          | File for deploying above app to k8s    |
| fluent_bit.yaml      | Container insight with CloudWatch |
