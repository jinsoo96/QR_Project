from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf.urls.static import static 
from django.conf import settings 

urlpatterns = [
    path('', views.home, name='home'),
    path('create_qr_code/', views.create_qr_code, name='create_qr_code'),
    path('result/<str:qr_code_path>/', views.result, name='result'),
    # 기타 필요한 URL 패턴
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
