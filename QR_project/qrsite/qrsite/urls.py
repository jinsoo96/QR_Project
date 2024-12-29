from django.contrib import admin
from django.urls import path, include  # 'include' 함수 추가
from polls import views
from asgiref.sync import async_to_sync
from qrsite import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', include('polls.urls')),  # 메인 페이지를 'polls' 앱의 홈 뷰로 리디렉션
]

# 개발 환경에서 정적 파일 경로 설정
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)







# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('polls/', include('polls.urls')),  # 'polls' 앱의 URL 포함
#     # 'your-url-path/' 경로의 필요성과 목적을 확인하세요.
#     path('', include('polls.urls')),  # 메인 페이지를 'polls' 앱의 홈 뷰로 리디렉션
#     path('create_qr_code/', views.create_qr_code, name='create_qr_code'), 
# ]

# # 개발 환경에서 정적 파일 경로 설정
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('your-url-path/', async_to_sync(views.some_view), name='some_view'),
#     path('polls/', include('polls.urls')),  # 'polls' 앱의 URL 포함
#     path('', views.home, name='home'),
#     path('create_qr_code/', views.create_qr_code, name='create_qr_code'), 
#     path('result/<str:qr_code_path>/', views.result, name='result'),

# ]

# # 개발 환경에서 정적 파일 경로 설정
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    
# #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)