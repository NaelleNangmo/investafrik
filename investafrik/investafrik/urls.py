"""
URL configuration for investafrik project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/auth/', include('apps.accounts.urls')),
    path('api/projects/', include('apps.projects.api_urls')),
    path('api/investments/', include('apps.investments.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    
    # Frontend URLs
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('how-it-works/', TemplateView.as_view(template_name='pages/how_it_works.html'), name='how_it_works'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('auth/', include('apps.accounts.frontend_urls')),
    path('investments/', include('apps.investments.frontend_urls')),
    path('messaging/', include('apps.messaging.frontend_urls')),
    
    # Admin dashboard
    path('admin/dashboard/', include('apps.accounts.admin_urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Customize admin
admin.site.site_header = "InvestAfrik Administration"
admin.site.site_title = "InvestAfrik Admin"
admin.site.index_title = "Tableau de bord"