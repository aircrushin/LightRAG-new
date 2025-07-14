### Setup (production)

```
docker compose up
```

### Setup (local)

```
# 启动后端服务
python -m lightrag.api.lightrag_server

# 前端
cd lightrag_webui
bun install
bun run dev
```

### neo4j

http://183.223.94.34:30061/browser/preview/
