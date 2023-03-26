# Running
## Setup
```bash
npm install -g pm2@latest
```

## Development
- Start the crawling process
    ```bash
    pm2 start start.sh
    ```
- View logs
    ```bash
    grc tail -f andromeda.log | grep "<regex-pattern>"
    ```
