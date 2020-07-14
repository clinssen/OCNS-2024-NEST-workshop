
Setup docker image with custom port for nest-server 

```
docker build -f ./cns20-nest-desktop.Dockerfile -t cns20-nest-desktop .
```

Start docker container
```
docker run -it -p 7000:5000 -p 7001:8000 cns20-nest-desktop
```

Go to ```http://localhost:7001```

