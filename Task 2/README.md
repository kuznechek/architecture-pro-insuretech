# Динамическое масштабирование контейнеров

## Часть 1. Динамическая маршрутизация на основании показателей утилизации памяти

```
cd ./2.1
```

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

[deployment.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/deployment.yaml)

[hpa.yaml](https://github.com/kuznechek/architecture-pro-insuretech/blob/insuretech/Task%202/hpa.yaml)

```
kubectl apply -f deployment.yaml
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
