# Динамическое масштабирование контейнеров

## Часть 1. Динамическая маршрутизация на основании показателей утилизации памяти

### Подготовка кластера

```
minikube start --driver=docker --cpus=2 --memory=4096
```
```
minikube status
```
```
minikube addons enable metrics-server
```

### Применение манифестов

[deployment.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/2.1/deployment.yaml)

[service.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/2.1/service.yaml)

[hpa.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/2.1/hpa.yaml)

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

###  Проброс порта 

`(В другом терминале)`

```
kubectl port-forward service/test-app-service 8080:8080
```

### Запуск Locust-скрипта

[locust.py](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/locust.py)

```
locust
```

### Мониторинг и демонстрация работы

**Вывод locust :**

[locust](http://localhost:8089)

![locust](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/src/locust.png)

```
kubectl get pods -w
```

![get pods](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/src/get_pods.png)

```
kubectl get hpa -w
```

![get hpa](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/src/get_hpa.png)

```
minikube dashboard
```

![dashboard](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/src/dashboard.png)

## Часть 2. Динамическая маршрутизация на основании показателей количества запросов в секунду

### Установка Prometheus в кластер

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
```
helm repo update
```
```
kubectl create namespace monitoring
```

# Установка kube-prometheus-stack

```
helm install prometheus prometheus-community/kube-prometheus-stack `
  --namespace monitoring `
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false `
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false
```

### Доступ к Prometheus Web UI

```
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-stack-prometheus 9090:9090
```

### Применение обновлённого манифеста

[deployment.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/2.2/deployment.yaml)

```
kubectl apply -f ../2.2/deployment.yaml
```

### Проверка метрик в Prometheus

[Prometheus Web UI](http://localhost:9090/targets)

![targets](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/src/targets.png)

### Установка Prometheus Adapter

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
```
helm install prometheus-adapter prometheus-community/prometheus-adapter `
  --namespace monitoring `
  --set prometheus.url=http://prometheus-kube-prometheus-stack-prometheus.monitoring:9090 `
  --set rules.default=false `
  --set rules.custom=[]
```

### Прмименение HPA на основе RPC


[hpa.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/2.2/hpa.yaml)

```
kubectl apply -f Task2/hpa-rps.yaml
```

### Запуск Locust-скрипта

```
locust
```

[locust](http://localhost:8089)
