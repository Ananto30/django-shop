from django.urls import path


from . import views

app_name = 'transaction'

urlpatterns = [
    path('sale/', views.sale, name='sale'),
]
