# Running
## Dev
```bash
flask --app api:run run --debug --host 0.0.0.0
```
## Prod
```bash
waitress-serve --call 'api:run'
```