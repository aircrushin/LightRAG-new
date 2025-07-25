# LightRAG 开发环境设置指南

## 环境要求

- Python 3.10+
- Poetry (Python 依赖管理)
- Bun (前端包管理器)

## 快速启动

### 1. 安装 Poetry 依赖

```bash
# 安装所有依赖，包括 API 相关的可选依赖
poetry install --extras api
```

### 2. 使用启动脚本

```bash
# 使用修改后的启动脚本（已配置使用 Poetry 虚拟环境）
./start_dev.sh
```

启动脚本会自动：
- 在 Poetry 虚拟环境中启动后端服务器
- 启动前端开发服务器
- 设置进程清理机制

### 3. 手动启动（可选）

如果需要分别启动前后端：

**后端服务器：**
```bash
# 使用 Poetry 虚拟环境
poetry run python -m lightrag.api.lightrag_server

# 或者激活虚拟环境后运行
poetry shell
python -m lightrag.api.lightrag_server
```

**前端开发服务器：**
```bash
cd lightrag_webui
bun run dev
```

## 虚拟环境信息

查看当前 Poetry 虚拟环境信息：
```bash
poetry env info
```

激活虚拟环境：
```bash
poetry shell
```

## 故障排除

### 1. 模块导入错误
如果遇到 `ModuleNotFoundError`，确保：
- 已运行 `poetry install --extras api`
- 使用 `poetry run` 命令或在激活的虚拟环境中运行

### 2. 依赖冲突
如果遇到依赖冲突：
```bash
# 重新安装依赖
poetry install --extras api --sync
```

### 3. 虚拟环境重建
如果需要重建虚拟环境：
```bash
# 删除现有虚拟环境
poetry env remove python

# 重新创建并安装依赖
poetry install --extras api
```

## 开发提示

- 使用 `poetry add <package>` 添加新的 Python 依赖
- 使用 `bun add <package>` 添加新的前端依赖
- 修改代码后，开发服务器会自动重载
- 后端 API 默认运行在 `http://localhost:8020`
- 前端开发服务器默认运行在 `http://localhost:5173`