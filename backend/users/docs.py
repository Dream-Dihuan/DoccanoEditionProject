"""
内部用户管理接口文档

本模块提供了用于内部系统集成的用户管理API文档。
这些接口只能通过在请求头中包含'dihuanKey: dihuan'来访问。
"""

# 接口文档
INTERNAL_USER_API_DOCS = {
    "title": "内部用户管理接口",
    "version": "v1",
    "description": "提供用户增删改查功能，仅供内部系统使用。所有请求必须在请求头中包含'dihuanKey: dihuan'",
    "authentication": "在请求头中添加 'dihuanKey: dihuan'",
    "endpoints": [
        {
            "method": "GET",
            "url": "/v1/internal/users/",
            "description": "获取用户列表",
            "parameters": [],
            "response": [
                {
                    "name": "id",
                    "type": "integer",
                    "description": "用户ID"
                },
                {
                    "name": "username",
                    "type": "string",
                    "description": "用户名"
                },
                {
                    "name": "is_superuser",
                    "type": "boolean",
                    "description": "是否为超级用户"
                },
                {
                    "name": "is_staff",
                    "type": "boolean",
                    "description": "是否为工作人员"
                }
            ],
            "example_request": "curl -H 'dihuanKey: dihuan' http://localhost:8000/v1/internal/users/",
            "example_response": """[
    {
        "id": 1,
        "username": "admin",
        "is_superuser": true,
        "is_staff": true
    },
    {
        "id": 2,
        "username": "testuser",
        "is_superuser": false,
        "is_staff": false
    }
]"""
        },
        {
            "method": "POST",
            "url": "/v1/internal/users/",
            "description": "创建新用户",
            "parameters": [
                {
                    "name": "username",
                    "required": True,
                    "type": "string",
                    "description": "用户名"
                },
                {
                    "name": "password",
                    "required": True,
                    "type": "string",
                    "description": "密码"
                },
                {
                    "name": "is_superuser",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为超级用户，默认为False"
                },
                {
                    "name": "is_staff",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为工作人员，默认为False"
                }
            ],
            "example_request": """curl -X POST -H "Content-Type: application/json" -H "dihuanKey: dihuan" \\
-d '{"username": "newuser", "password": "password123", "is_superuser": false, "is_staff": false}' \\
http://localhost:8000/v1/internal/users/""",
            "example_response": """{
    "id": 3,
    "username": "newuser",
    "is_superuser": false,
    "is_staff": false
}"""
        },
        {
            "method": "GET",
            "url": "/v1/internal/users/{id}/",
            "description": "获取特定用户信息",
            "parameters": [
                {
                    "name": "id",
                    "required": True,
                    "type": "integer",
                    "description": "用户ID"
                }
            ],
            "example_request": "curl -H 'dihuanKey: dihuan' http://localhost:8000/v1/internal/users/1/",
            "example_response": """{
    "id": 1,
    "username": "admin",
    "is_superuser": true,
    "is_staff": true
}"""
        },
        {
            "method": "PUT",
            "url": "/v1/internal/users/{id}/",
            "description": "更新特定用户信息（全量更新）",
            "parameters": [
                {
                    "name": "id",
                    "required": True,
                    "type": "integer",
                    "description": "用户ID"
                },
                {
                    "name": "username",
                    "required": True,
                    "type": "string",
                    "description": "用户名"
                },
                {
                    "name": "password",
                    "required": False,
                    "type": "string",
                    "description": "密码"
                },
                {
                    "name": "is_superuser",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为超级用户"
                },
                {
                    "name": "is_staff",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为工作人员"
                }
            ],
            "example_request": """curl -X PUT -H "Content-Type: application/json" -H "dihuanKey: dihuan" \\
-d '{"username": "updateduser", "is_superuser": true, "is_staff": true}' \\
http://localhost:8000/v1/internal/users/1/""",
            "example_response": """{
    "id": 1,
    "username": "updateduser",
    "is_superuser": true,
    "is_staff": true
}"""
        },
        {
            "method": "PATCH",
            "url": "/v1/internal/users/{id}/",
            "description": "部分更新特定用户信息",
            "parameters": [
                {
                    "name": "id",
                    "required": True,
                    "type": "integer",
                    "description": "用户ID"
                },
                {
                    "name": "username",
                    "required": False,
                    "type": "string",
                    "description": "用户名"
                },
                {
                    "name": "password",
                    "required": False,
                    "type": "string",
                    "description": "密码"
                },
                {
                    "name": "is_superuser",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为超级用户"
                },
                {
                    "name": "is_staff",
                    "required": False,
                    "type": "boolean",
                    "description": "是否为工作人员"
                }
            ],
            "example_request": """curl -X PATCH -H "Content-Type: application/json" -H "dihuanKey: dihuan" \\
-d '{"is_staff": true}' \\
http://localhost:8000/v1/internal/users/1/""",
            "example_response": """{
    "id": 1,
    "username": "updateduser",
    "is_superuser": true,
    "is_staff": true
}"""
        },
        {
            "method": "DELETE",
            "url": "/v1/internal/users/{id}/",
            "description": "删除特定用户",
            "parameters": [
                {
                    "name": "id",
                    "required": True,
                    "type": "integer",
                    "description": "用户ID"
                }
            ],
            "example_request": "curl -X DELETE -H 'dihuanKey: dihuan' http://localhost:8000/v1/internal/users/1/",
            "example_response": ""
        }
    ],
    "error_responses": [
        {
            "status_code": 403,
            "description": "未提供有效的dihuanKey",
            "example_response": """{
    "detail": "您没有执行该操作的权限。"
}"""
        },
        {
            "status_code": 404,
            "description": "请求的用户不存在",
            "example_response": """{
    "detail": "未找到。"
}"""
        }
    ]
}
"""
用户管理API文档

本模块提供外部系统管理doccano用户的API接口文档说明。
所有接口均需要身份验证，且根据操作类型需要不同的权限：
- 列表查询：项目管理员或超级用户权限
- 创建/更新/删除：仅超级用户权限
"""

# 接口文档
USER_API_DOCS = {
    "title": "用户管理接口",
    "description": "提供用户增删改查功能的外部API接口",
    "version": "v1",
    "base_url": "/v1/external/external-users/",
    "endpoints": {
        "list": {
            "method": "GET",
            "url": "/v1/external/external-users/",
            "name": "用户列表",
            "description": "获取系统中所有用户的列表信息",
            "parameters": {
                "search": {
                    "in": "query",
                    "type": "string",
                    "required": False,
                    "description": "按用户名搜索用户"
                }
            },
            "responses": {
                "200": {
                    "description": "成功返回用户列表",
                    "schema": [
                        {
                            "id": "integer",
                            "username": "string",
                            "is_superuser": "boolean",
                            "is_staff": "boolean"
                        }
                    ]
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                }
            },
            "example_request": "GET /v1/external/external-users/",
            "example_response": [
                {
                    "id": 1,
                    "username": "admin",
                    "is_superuser": True,
                    "is_staff": True
                },
                {
                    "id": 2,
                    "username": "user1",
                    "is_superuser": False,
                    "is_staff": False
                }
            ]
        },
        "create": {
            "method": "POST",
            "url": "/v1/external/external-users/",
            "name": "创建用户",
            "description": "创建一个新的用户",
            "parameters": {
                "body": {
                    "in": "body",
                    "required": True,
                    "schema": {
                        "username": {
                            "type": "string",
                            "required": True,
                            "description": "用户名"
                        },
                        "password": {
                            "type": "string",
                            "required": True,
                            "description": "用户密码"
                        },
                        "is_superuser": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为超级用户，默认为False"
                        },
                        "is_staff": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为工作人员，默认为False"
                        }
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "用户创建成功",
                    "schema": {
                        "id": "integer",
                        "username": "string",
                        "is_superuser": "boolean",
                        "is_staff": "boolean"
                    }
                },
                "400": {
                    "description": "请求参数错误"
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                }
            },
            "example_request": {
                "url": "POST /v1/external/external-users/",
                "body": {
                    "username": "newuser",
                    "password": "password123",
                    "is_staff": True
                }
            },
            "example_response": {
                "id": 3,
                "username": "newuser",
                "is_superuser": False,
                "is_staff": True
            }
        },
        "retrieve": {
            "method": "GET",
            "url": "/v1/external/external-users/{id}/",
            "name": "获取用户详情",
            "description": "根据用户ID获取特定用户的详细信息",
            "parameters": {
                "id": {
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "用户ID"
                }
            },
            "responses": {
                "200": {
                    "description": "成功返回用户详情",
                    "schema": {
                        "id": "integer",
                        "username": "string",
                        "is_superuser": "boolean",
                        "is_staff": "boolean"
                    }
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                },
                "404": {
                    "description": "用户不存在"
                }
            },
            "example_request": "GET /v1/external/external-users/1/",
            "example_response": {
                "id": 1,
                "username": "admin",
                "is_superuser": True,
                "is_staff": True
            }
        },
        "update": {
            "method": "PUT",
            "url": "/v1/external/external-users/{id}/",
            "name": "更新用户",
            "description": "更新指定用户的详细信息",
            "parameters": {
                "id": {
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "用户ID"
                },
                "body": {
                    "in": "body",
                    "required": True,
                    "schema": {
                        "username": {
                            "type": "string",
                            "required": False,
                            "description": "用户名"
                        },
                        "password": {
                            "type": "string",
                            "required": False,
                            "description": "用户密码"
                        },
                        "is_superuser": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为超级用户"
                        },
                        "is_staff": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为工作人员"
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "用户更新成功",
                    "schema": {
                        "id": "integer",
                        "username": "string",
                        "is_superuser": "boolean",
                        "is_staff": "boolean"
                    }
                },
                "400": {
                    "description": "请求参数错误"
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                },
                "404": {
                    "description": "用户不存在"
                }
            },
            "example_request": {
                "url": "PUT /v1/external/external-users/1/",
                "body": {
                    "username": "updated_admin",
                    "is_staff": True
                }
            },
            "example_response": {
                "id": 1,
                "username": "updated_admin",
                "is_superuser": True,
                "is_staff": True
            }
        },
        "partial_update": {
            "method": "PATCH",
            "url": "/v1/external/external-users/{id}/",
            "name": "部分更新用户",
            "description": "部分更新指定用户的详细信息",
            "parameters": {
                "id": {
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "用户ID"
                },
                "body": {
                    "in": "body",
                    "required": True,
                    "schema": {
                        "username": {
                            "type": "string",
                            "required": False,
                            "description": "用户名"
                        },
                        "password": {
                            "type": "string",
                            "required": False,
                            "description": "用户密码"
                        },
                        "is_superuser": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为超级用户"
                        },
                        "is_staff": {
                            "type": "boolean",
                            "required": False,
                            "description": "是否为工作人员"
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "用户更新成功",
                    "schema": {
                        "id": "integer",
                        "username": "string",
                        "is_superuser": "boolean",
                        "is_staff": "boolean"
                    }
                },
                "400": {
                    "description": "请求参数错误"
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                },
                "404": {
                    "description": "用户不存在"
                }
            },
            "example_request": {
                "url": "PATCH /v1/external/external-users/1/",
                "body": {
                    "is_staff": False
                }
            },
            "example_response": {
                "id": 1,
                "username": "admin",
                "is_superuser": True,
                "is_staff": False
            }
        },
        "destroy": {
            "method": "DELETE",
            "url": "/v1/external/external-users/{id}/",
            "name": "删除用户",
            "description": "删除指定用户",
            "parameters": {
                "id": {
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "用户ID"
                }
            },
            "responses": {
                "204": {
                    "description": "用户删除成功"
                },
                "401": {
                    "description": "未认证"
                },
                "403": {
                    "description": "权限不足"
                },
                "404": {
                    "description": "用户不存在"
                }
            },
            "example_request": "DELETE /v1/external/external-users/1/",
            "example_response": ""
        }
    },
    "authentication": {
        "type": "Token",
        "description": "所有请求都需要在Authorization头中包含有效的认证令牌",
        "example": "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    },
    "permissions": {
        "list": "项目管理员或超级用户",
        "create": "超级用户",
        "retrieve": "项目管理员或超级用户",
        "update": "超级用户",
        "partial_update": "超级用户",
        "destroy": "超级用户"
    }
}