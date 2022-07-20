# Deploy
## Dockerfile
```
docker build -t grass .
docker run -p 9001:9001 --name grass-container -d grass
```
Optionals
```
docker exec -it grass-container /bin/bash
docker logs -f grass-container
```
