from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DoccanoAdminSite(admin.AdminSite):
    site_header = _('跨文档关联标注工具-管理页面')
    site_title = _('跨文档关联标注工具-管理页面')
    index_title = _('跨文档关联标注工具-管理页面')


# 创建自定义AdminSite实例
doccano_admin_site = DoccanoAdminSite(name='admin')