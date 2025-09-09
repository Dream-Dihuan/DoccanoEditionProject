# 外部用户管理API文档## 安全警告

此API接口无需认证即可访问，因此：

1. 请确保该接口只能在受信任的网络环境中访问
2. 不要在公共网络或不安全的网络环境中暴露此接口
3. 建议通过网络防火墙或反向代理限制对此接口的访问
4. 生产环境中应考虑添加适当的认证和权限控制机制

## 概述

本文档详细说明了doccano系统的外部用户管理API接口。这些接口允许通过RESTful API对doccano用户进行增删改查操作，无需认证和权限验证。

## 基础信息

- **API版本**: v1
- **基础URL**: `/v1/external/external-users/`
- **数据格式**: JSON
- **认证**: 无需认证（请确保只能在受信任的网络环境中访问）

## API接口详情

### 1. 获取用户列表

**请求方法**: `GET`

**请求URL**: `/v1/external/external-users/`

**请求参数**:
- `search` (可选): 按用户名搜索用户

**响应状态码**:
- 200: 成功

**请求示例**:
```bash
curl http://localhost:8000/v1/external/external-users/
```

**响应示例**:
```json
[
    {
        "id": 1,
        "username": "admin",
        "is_superuser": true,
        "is_staff": true
    },
    {
        "id": 2,
        "username": "user1",
        "is_superuser": false,
        "is_staff": false
    }
]
```

### 2. 创建用户

**请求方法**: `POST`

**请求URL**: `/v1/external/external-users/`

**请求体参数**:
- `username` (必需): 用户名
- `password` (必需): 用户密码
- `is_superuser` (可选): 是否为超级用户，默认为false
- `is_staff` (可选): 是否为工作人员，默认为false

**响应状态码**:
- 201: 创建成功
- 400: 请求参数错误

**请求示例**:
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username":"newuser", "password":"password123", "is_staff":true}' \
     http://localhost:8000/v1/external/external-users/
```

**响应示例**:
```json
{
    "id": 3,
    "username": "newuser",
    "is_superuser": false,
    "is_staff": true
}
```

### 3. 获取用户详情

**请求方法**: `GET`

**请求URL**: `/v1/external/external-users/{id}/`

**路径参数**:
- `id`: 用户ID

**响应状态码**:
- 200: 成功
- 404: 用户不存在

**请求示例**:
```bash
curl http://localhost:8000/v1/external/external-users/1/
```

**响应示例**:
```json
{
    "id": 1,
    "username": "admin",
    "is_superuser": true,
    "is_staff": true
}
```

### 4. 更新用户

**请求方法**: `PUT`

**请求URL**: `/v1/external/external-users/{id}/`

**路径参数**:
- `id`: 用户ID

**请求体参数**:
- `username` (可选): 用户名
- `password` (可选): 用户密码
- `is_superuser` (可选): 是否为超级用户
- `is_staff` (可选): 是否为工作人员

**响应状态码**:
- 200: 更新成功
- 400: 请求参数错误
- 404: 用户不存在

**请求示例**:
```bash
curl -X PUT \
     -H "Content-Type: application/json" \
     -d '{"username":"updated_admin", "is_staff":true}' \
     http://localhost:8000/v1/external/external-users/1/
```

**响应示例**:
```json
{
    "id": 1,
    "username": "updated_admin",
    "is_superuser": true,
    "is_staff": true
}
```

### 5. 部分更新用户

**请求方法**: `PATCH`

**请求URL**: `/v1/external/external-users/{id}/`

**路径参数**:
- `id`: 用户ID

**请求体参数**:
- `username` (可选): 用户名
- `password` (可选): 用户密码
- `is_superuser` (可选): 是否为超级用户
- `is_staff` (可选): 是否为工作人员

**响应状态码**:
- 200: 更新成功
- 400: 请求参数错误
- 404: 用户不存在

**请求示例**:
```bash
curl -X PATCH \
     -H "Content-Type: application/json" \
     -d '{"is_staff":false}' \
     http://localhost:8000/v1/external/external-users/1/
```

**响应示例**:
```json
{
    "id": 1,
    "username": "admin",
    "is_superuser": true,
    "is_staff": false
}
```

### 6. 删除用户

**请求方法**: `DELETE`

**请求URL**: `/v1/external/external-users/{id}/`

**路径参数**:
- `id`: 用户ID

**响应状态码**:
- 204: 删除成功
- 404: 用户不存在

**请求示例**:
```bash
curl -X DELETE \
     -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/v1/external/external-users/1/
```

## 错误响应

API可能返回以下错误状态码：

| 状态码 | 描述 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

错误响应格式示例：
```json
{
    "detail": "用户不存在。"
}
```