# Start local server
```

uvicorn parenting.app:app --host 0.0.0.0 --port 5001 --reload

```

# Deploy Procfile
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```