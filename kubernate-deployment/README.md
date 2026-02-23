
docker build -t backend:latest .\backend\


docker build -t frontend:latest .\frontend\


kubectl apply -f namespace.yaml
kubectl apply -f .\backend\backend-deployment.yaml
kubectl apply -f .\frontend\frontend-deployment.yaml
kubectl apply -f .\backend\backend-service.yaml
kubectl apply -f .\frontend\frontend-service.yaml




kubectl get pods









# View logs of a pod
kubectl logs -n soil-app deployment/backend
kubectl logs -n soil-app deployment/frontend

# Describe a pod for error details
kubectl describe pod -n soil-app -l app=backend

# Delete everything and redeploy
kubectl delete namespace soil-app
kubectl apply -f namespace.yaml -f backend\ -f frontend\