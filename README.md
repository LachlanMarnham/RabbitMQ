Build the Docker image

```console
docker build -t rabbit_mq .
```

Run the image and open a shell

```console
docker exec -it $(docker run -d -p 5672:5672 rabbit_mq) /bin/bash
```

Now RabbitMQ will be listening (via the container port) on localhost:5672
