from django.urls import path, include
from .views import main, dashboard, chart_data, test, chart_data_v2, DataItemViewSet, pH_valueViewSet
from rest_framework import routers

app_name = 'my_app'

router = routers.DefaultRouter()
router.register('data_item', DataItemViewSet, basename="data_item" )

router.register('pH_value', pH_valueViewSet, basename="pH_value" )

urlpatterns = [
    path('', main, name='main'),
    path('graph/', test, name='graph'),
    path('<slug>/',dashboard, name='dashboard'),
    path('<slug>/chart/', chart_data_v2, name='chart'),
    #path('graph/chart/', chart_data_v2 , name='chart_v2'),
   # path('api/data/', SensorDataAPIView.as_view(), name='sensor-data'),



    path('api/', include(router.urls)),
    
]