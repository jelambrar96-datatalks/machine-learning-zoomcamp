## Homework [DRAFT]

In this homework, we'll deploy the credit scoring model from the homework 5.
We already have a docker image for this model - we'll use it for 
deploying the model to Kubernetes.


## Bulding the image

Clone the course repo if you haven't:

```
git clone https://github.com/DataTalksClub/machine-learning-zoomcamp.git
```

Go to the `course-zoomcamp/cohorts/2023/05-deployment/homework` folder and 
execute the following:


```bash
docker build -t zoomcamp-model:hw10 .
```

> **Note:** If you have troubles building the image, you can 
> use the image we built and published to docker hub:
> `docker pull svizor/zoomcamp-model:hw10`


## Question 1

Run it to test that it's working locally:

```bash
docker run -it --rm -p 9696:9696 zoomcamp-model:hw10
```

And in another terminal, execute `q6_test.py` file:

```bash
python q6_test.py
```

You should see this:

```python
{'get_credit': True, 'get_credit_probability': <value>}
```

Here `<value>` is the probability of getting a credit card. You need to choose the right one.

* 0.3269
* **0.5269** (answer)
* 0.7269
* 0.9269

```bash
$ python3 q6_test.py 
{'has_subscribed': True, 'has_subscribed_probability': 0.5777958281673269}
```

Now you can stop the container running in Docker.


## Installing `kubectl` and `kind`

You need to install:

* `kubectl` - https://kubernetes.io/docs/tasks/tools/ (you might already have it - check before installing)
* `kind` - https://kind.sigs.k8s.io/docs/user/quick-start/


## Question 2

What's the version of `kind` that you have? 

Use `kind --version` to find out.

``` kind --version 
kind version 0.25.0
```

## Creating a cluster

Now let's create a cluster with `kind`:

```bash
kind create cluster
```

```bash
$ kind create cluster 
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.31.2) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Not sure what to do next? 😅  Check out https://kind.sigs.k8s.io/docs/user/quick-start/
```

And check with `kubectl` that it was successfully created:

```bash
kubectl cluster-info
```

```bash
$ kubectl cluster-info 
Kubernetes control plane is running at https://127.0.0.1:44593
CoreDNS is running at https://127.0.0.1:44593/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Question 3

Now let's test if everything works. Use `kubectl` to get the list of running services. 

What's `CLUSTER-IP` of the service that is already running there? 


```bash
$$ kubectl get services 
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   34m
```

```
10.96.0.1
```

## Question 4

To be able to use the docker image we previously created (`zoomcamp-model:hw10`),
we need to register it with `kind`.

What's the command we need to run for that?

* `kind create cluster`
* `kind build node-image`
* **`kind load docker-image`** (answer)
* `kubectl apply`

```bash
$ kind load docker-image zoomcamp-model:3.11.5-hw10 
Image: "zoomcamp-model:3.11.5-hw10" with ID "sha256:ef37a6e599cd40a2dd5fe66331e16b5ef521e3846a81df576b64ba2854a6fa87" not yet present on node "kind-control-plane", loading...
```

## Question 5

Now let's create a deployment config (e.g. `deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: credit
spec:
  selector:
    matchLabels:
      app: credit
  replicas: 1
  template:
    metadata:
      labels:
        app: credit
    spec:
      containers:
      - name: credit
        image: <Image>
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"            
          limits:
            memory: <Memory>
            cpu: <CPU>
        ports:
        - containerPort: <Port>
```

Replace `<Image>`, `<Memory>`, `<CPU>`, `<Port>` with the correct values.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: credit
spec:
  selector:
    matchLabels:
      app: credit
  replicas: 1
  template:
    metadata:
      labels:
        app: credit
    spec:
      containers:
      - name: credit
        image: zoomcamp-model:3.11.5-hw10
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"            
          limits:
            memory: "512Mi"
            cpu: "500m"
        ports:
        - containerPort: 9696
```

What is the value for `<Port>`?

```
9696
```

Apply this deployment using the appropriate command and get a list of running Pods. 
You can see one running Pod.


```bash
kubectl apply -f deployment.yaml
```

```bash
$ kubectl get pods 
NAME                      READY   STATUS    RESTARTS   AGE
credit-6cdf9545d4-dl4x4   1/1     Running   0          70s
```


## Question 6

Let's create a service for this deployment (`service.yaml`):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: <Service name>
spec:
  type: LoadBalancer
  selector:
    app: <???>
  ports:
  - port: 80
    targetPort: <PORT>
```

Fill it in. What do we need to write instead of `<???>`?


```yaml
apiVersion: v1
kind: Service
metadata:
  name: credit
spec:
  type: LoadBalancer
  selector:
    app: credit
  ports:
  - port: 80
    targetPort: 9696
```

Apply this config file.


```bash
$ kubectl get services
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
credit       LoadBalancer   10.96.239.12   <pending>     80:32411/TCP   15s
kubernetes   ClusterIP      10.96.0.1      <none>        443/TCP        120m
```


## Testing the service

We can test our service locally by forwarding the port 9696 on our computer 
to the port 80 on the service:

```bash
kubectl port-forward service/<Service name> 9696:80
```

```bash
$ kubectl port-forward service/credit 9696:80
Forwarding from 127.0.0.1:9696 -> 9696
Forwarding from [::1]:9696 -> 9696
Handling connection for 9696
```


Run `q6_test.py` (from the homework 5) once again to verify that everything is working. 
You should get the same result as in Question 1.

```bash
$ python3 q6_test.py 
{'has_subscribed': True, 'has_subscribed_probability': 0.5777958281673269}
```


## Autoscaling

Now we're going to use a [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) 
(HPA for short) that automatically updates a workload resource (such as our deployment), 
with the aim of automatically scaling the workload to match demand.

Use the following command to create the HPA:

```bash
kubectl autoscale deployment credit --name credit-hpa --cpu-percent=20 --min=1 --max=3
```

```bash
$ kubectl autoscale deployment credit --name credit-hpa --cpu-percent=20 --min=1 --max=3 
horizontalpodautoscaler.autoscaling/credit-hpa autoscaled
```

You can check the current status of the new HPA by running:

```bash
kubectl get hpa
```

The output should be similar to the next:

```bash
NAME              REFERENCE                TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
credit-hpa   Deployment/credit   1%/20%    1         3         1          27s
```

Current output: 

```bash
$ kubectl get hpa 
NAME         REFERENCE           TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
credit-hpa   Deployment/credit   cpu: <unknown>/20%   1         3         1          34s
```

`TARGET` column shows the average CPU consumption across all the Pods controlled by the corresponding deployment.
Current CPU consumption is about 0% as there are no clients sending requests to the server.
> 
>Note: In case the HPA instance doesn't run properly, try to install the latest Metrics Server release 
> from the `components.yaml` manifest:
> ```bash
> kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
>```


## Increase the load

Let's see how the autoscaler reacts to increasing the load. To do this, we can slightly modify the existing
`q6_test.py` script by putting the operator that sends the request to the credit service into a loop.

```python
while True:
    sleep(0.1)
    response = requests.post(url, json=client).json()
    print(response)
```


```python
from time import sleep
import requests


url = "http://localhost:9696/predict"
client = {"job": "management", "duration": 400, "poutcome": "success"}

while True:
    sleep(0.1)
    response = requests.post(url, json=client).json()
    print(response)
```


Now you can run this script.


## Question 7 (optional)

Run `kubectl get hpa credit-hpa --watch` command to monitor how the autoscaler performs. 
Within a minute or so, you should see the higher CPU load; and then - more replicas. 
What was the maximum amount of the replicas during this test?


* **1** (answer)
* 2
* 3
* 4


```bash
$ kubectl get hpa credit-hpa --watch 
NAME         REFERENCE           TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
credit-hpa   Deployment/credit   cpu: <unknown>/20%   1         3         1          8m27s
```

> Note: It may take a few minutes to stabilize the number of replicas. Since the amount of load is not controlled 
> in any way it may happen that the final number of replicas will differ from initial.

## Submit the results

* Submit your results here: TBA
* If your answer doesn't match options exactly, select the closest one
