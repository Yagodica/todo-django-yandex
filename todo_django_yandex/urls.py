from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todolist.urls')),
    path('todo_auth/', include('todo_auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]