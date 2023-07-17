from django.urls import path,include
from .views import SignUp,IndexView,ProfileView,FAQ,UpdateChartDataView,add_metatrader_account,switch_metatrader_account,account_list
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('signup/',SignUp.as_view(), name='signup'),
    path('FAQ/',FAQ.as_view(), name='faq'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('add/', add_metatrader_account, name='add_metatrader_account'),
    path('list/', account_list, name='account_list'),
    path('switch_account/<int:account_id>/', switch_metatrader_account, name='switch_metatrader_account'),
    path('update-chart-data/', UpdateChartDataView.as_view(), name='update_chart_data'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/', include('allauth.urls')),
]
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
handler404 = 'Dashboard.views.error_404_view'
handler500 = 'Dashboard.views.error_500'