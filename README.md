# fastapi-template
FastAPI simple template

# Deploy
## Dockerfile
```
docker build -t fastapi-template .
docker run -p 9001:9001 --name fastapi-template-container -d fastapi-template
```
Optionals
```
docker exec -it fastapi-template-container /bin/bash
docker logs -f fastapi-template-container
```