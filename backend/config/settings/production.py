from .base import *  # noqa: F401,F403

DEBUG = False

# 添加安全头配置
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# 允许所有来源（仅用于开发环境，生产环境应明确指定）
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# 允许所有主机
ALLOWED_HOSTS = ["*"]

# 添加静态文件配置
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s::%(funcName)s::%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}