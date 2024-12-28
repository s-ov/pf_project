from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView 


admin.site.site_header = "Energy Unit's Admin"

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        '', 
         TemplateView.as_view(template_name='index.html'), 
         name='main_page'
         ),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('work_tower/', include(('work_tower.urls', 'work_tower'), namespace='work_tower')),
    path('task/', include(('task.urls', 'task'), namespace='task')),
    path('workflow/', include(('workflow.urls', 'workflow'), namespace='workflow')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
