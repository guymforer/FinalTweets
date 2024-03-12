# Twitter Data Insight Service 📊

The Twitter Data Insight Service is designed to provide comprehensive analytics and insights into Twitter data. It focuses on tweet distributions, sentiment analysis, top tweets, and user activity. The service is containerized for deployment within a Kubernetes (k8s) cluster, ensuring scalability and ease of management.

## Getting Started 🚀

This guide covers setting up and running the Twitter Data Insight Service on a local Kubernetes cluster using Minikube.

### Prerequisites 🛠️

Ensure you have the following installed:
- Minikube
- kubectl
- Docker (optional for image creation)

### Install Minikube

Install Minikube based on your operating system:

```sh
# macOS
brew install minikube

# Windows/Linux
pip install minikube
```

### Start Minikube 🌟

Initialize your Minikube cluster:

```sh
minikube start
```

### Enable Ingress Controller 🖌️

Activate Minikube's Ingress controller to route external traffic to services:

```sh
minikube addons enable ingress
```

### Create Namespace

Generate a dedicated namespace for your application's resources:

```sh
kubectl create namespace tweets
```

### Deploy the Application

Deploy the application and its related resources:

```sh
kubectl apply -f ./k8s -n tweets
```

## Accessing the Frontend 🌐

To access the application, use one of the following methods:

### Minikube Tunnel

Start a tunnel to allow Ingress resources:

```sh
minikube tunnel
```

### Hosts File

Update `/etc/hosts` (or equivalent on Windows) to map the application domain to `127.0.0.1`:

```
127.0.0.1 twitterdatainsight.com
```

### Browser Access

Visit `http://twitterdatainsight.com` in your web browser.

Alternatively, explore deployment details using:

```sh
minikube dashboard
```

## Usage 📊

- **Option 1:** Enter an author's name for a sentiment distribution graph of their tweets.
- **Option 2:** View a graph showing tweet volumes by all authors.
- **Option 3:** Discover top tweets by likes and shares.
- **Option 4:** Find top users by content volume.

## Cleanup 🧹

Remove resources and stop Minikube:

```sh
kubectl delete namespace tweets
minikube stop
minikube delete
```

Thank you for exploring the Twitter Data Insight Service. For support or feedback, please contact our team.
# FinalTweets
