### Сборка образа

```bash
docker build ./ --phones
```

### Запуск контейнера

```bash
docker run --name my_phones -d -p 8000:8000 phones
```