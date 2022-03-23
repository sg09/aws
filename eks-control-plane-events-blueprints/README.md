# Managing Amazon EKS control plane events


## Context
Currently EKS event TTL is set to 60m. Some customers have shown interest to increase the TTL. (https://github.com/aws/containers-roadmap/issues/785). It will be an additional burden if EKS control plane provided the option to increase TTL as this will add load to ETCD and storage. This solution here tries to bridge the gap to capture events beyond 60 minutes to cloudwatch, if the customers still achieve the same. That way control plane event TTL is not modified but at the sametime, if customer wanted to capture the events beyond 60m, they could achieve the same.


## Prerequisites

For this walkthrough, you should have the following prerequisites: 

* An AWS account 
* Running AWS EKS cluster 
* Basic Kubernetes knowledge (Pods, namespace and deployments)

## Solution flow

![This is a alt text.](/image/sample.png "This is a sample image.")

