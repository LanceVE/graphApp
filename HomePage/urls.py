from django.urls import path
from .views import new_home, new_processing_view, upload_graph, graph_list
from django.conf.urls.static import static
from django.conf import settings


#URLCONF

urlpatterns = [
   path('', new_home, name = 'home'), 
   path('processing/', new_processing_view, name = 'processing'),
   # path('upload/', upload , name = 'upload'),
   path('graph/', graph_list , name = 'graph_list'),
   path('graph/upload/', upload_graph , name = 'upload_graph'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)