"""SinDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler403, handler500
from django.conf import settings
from django.contrib.auth.decorators import login_required

from account import urls as account_urls
from db_query import urls as db_query_urls
from db_manage import urls as db_manage_urls
from SinDB.views import index_view, not_permission
from SinDB.zjxl_sso_client import Client, sso_log_out

from libs.base_url_required import required, superuser_required

zjxl_sso = Client(settings.SSO_LOGIN_SERVER, settings.SSO_PUB_KEY, settings.SSO_PRI_KEY)

# 默认的handler 使用的是template 下 404.html 暂时不需要重写，就直接用默认的。
handler403 = handler403
handler404 = handler404
handler500 = handler500

# 不需要登录的
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page_not_permission/', not_permission, name="not_permission"),
    path('login', include(zjxl_sso.get_login_urls())),
]

# 需要管理员用户才可以访问的
urlpatterns_admin = [
    path('account/', include(account_urls)),
    path('databases/', include(db_manage_urls)),
]

# 需要登录才可以操作的
urlpatterns_login = [
    path('', index_view),
    path('sql_query/', include(db_query_urls)),
    path('logout', sso_log_out, name="logout"),
]

urlpatterns += required(
    (login_required, superuser_required(login_url="not_permission")),
    urlpatterns_admin
)
urlpatterns += required(
    login_required,
    urlpatterns_login
)
