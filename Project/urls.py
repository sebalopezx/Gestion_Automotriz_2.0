"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

# from Management.views import signin
from apps.Management.views import IndexView, SignupView, SigninView, SignoutView, ListUserDataView, DetailuserData, DeleteUserView, UpdatePassword
from apps.Management.views import RegisterVehicleView, UpdateVehicleView, RegisterDateView, CreateCouponPointsView, DeleteCouponView, ListVehiclesView, DeleteVehicleView, StateVehicleView, ListAppointmentView, CancelAppointmentView
from apps.Management.views import RegisterRecepcionistView, ListMechanicView, RegisterMechanicView, UpdateMechanicView, DeleteMechanicView, ListJobsDiaryView, ListJobsInProgressView, ChangeMechanicInJobView, ListJobsCompletedView, JobChecklistView, DeleteServiceView, UpdateJobView, DeleteJobView, CompleteJobView, SearchPatentView
from apps.Management import views
from apps.Management import api
# from Management.api import obtener_marcas_y_modelos, VehicleDataAPIView

urlpatterns = [
    path('admin/', admin.site.urls, name="administration"),
    path('', IndexView.as_view(), name='index' ),

    path('api/', api.api_vehicles, name='vehicles' ),
    path('api/brands/', api.get_brands, name='brands' ),
    path('api/brands/<str:object_id_marca>/', api.get_models, name='models' ),
    path('api/brands/<str:object_id_marca>/models/<str:object_id_modelo>/', api.get_years, name='years' ),


    # URLS LOGIN
    path('signin/', SigninView.as_view(), name='signin' ),
    path('signup/', SignupView.as_view(), name='signup' ),
    path('signout/', SignoutView.as_view(), name='signout' ),

    # URLS CLIENTES 
    path('user_data/', ListUserDataView.as_view() , name='user_data'),
    path('user_data/<int:id>/data/', DetailuserData.as_view() , name='detail_user_data'),
    path('user_data/<int:id>/update/', UpdatePassword.as_view(), name='update_password'),
    path('user_data/<int:id>/delete_user/', DeleteUserView.as_view(), name='delete_user'),

    path('user_data/create_coupon_points/', CreateCouponPointsView.as_view(), name='create_coupon_points'),
    path('user_data/<int:id>/delete_coupon/', DeleteCouponView.as_view(), name='delete_coupon'),

    path('vehicle/', ListVehiclesView.as_view(), name='vehicle'),
    path('vehicle/<int:id>/state/', StateVehicleView.as_view(), name='state_vehicle'),
    path('vehicle/<int:id>/delete/', DeleteVehicleView.as_view(), name='delete_vehicle'),
    path('vehicle/<int:id>/update/', UpdateVehicleView.as_view(), name='update_vehicle'),
    path('register_vehicle/', RegisterVehicleView.as_view(), name='register_vehicle'),

    path('appointment/', ListAppointmentView.as_view(), name='appointment'),
    path('appointment/<int:id>/cancel/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('register_date/', RegisterDateView.as_view(), name='register_date'),

    # path('points/', views.points, name='points'),


    # URLS RECEPCIONISTAS
    # path('register_recepcionist/', views.register_recepcionist ,name='register_recepcionist'),
    # path('gestion_coupons/', views.gestion_coupons, name='gestion_coupons'),

    path('list_mechanic/', ListMechanicView.as_view(), name='list_mechanic'),
    path('list_mechanic/<int:id>/update/', UpdateMechanicView.as_view(), name='update_mechanic'),
    path('list_mechanic/<int:id>/delete/', DeleteMechanicView.as_view(), name='delete_mechanic'),
    path('register_mechanic/', RegisterMechanicView.as_view(), name='register_mechanic'),

    # path('list_jobs_pending/', views.list_jobs_pending ,name='list_jobs_pending'),
    # path('list_jobs_pending/<int:id>/ot/', views.generate_ot ,name='generate_ot'),
    # path('list_jobs_pending/<int:id>/delete/<str:job_type>/', views.delete_job ,name='delete_job_pending'),

    path('change_mechanic/<int:id>/', ChangeMechanicInJobView.as_view(), name='change_mechanic'),
    path('list_jobs_diary/', ListJobsDiaryView.as_view(), name='list_jobs_diary'),
    path('list_jobs_inprogress/', ListJobsInProgressView.as_view(), name='list_jobs_inprogress'),
    path('list_jobs_inprogress/<int:id>/checklist/', JobChecklistView.as_view(), name='checklist'),
    path('list_jobs_inprogress/<int:id>/update/', UpdateJobView.as_view(), name='update_job'),
    path('list_jobs_inprogress/<int:id>/<str:job_type>/delete/', DeleteJobView.as_view(), name='delete_job_inprogress'),
    path('list_jobs_inprogress/<int:id>/completed/', CompleteJobView.as_view(), name='completed_job'), # TODO: NOMBRE MAS DESCRIPTIVO 
    path('list_jobs_completed/', ListJobsCompletedView.as_view(), name='list_jobs_completed'),
    path('list_jobs_completed/<int:id>/<str:job_type>/delete/', DeleteJobView.as_view(), name='delete_job_completed'),
    path('list_service/<int:id_service>/<int:id>/delete/', DeleteServiceView.as_view(), name='delete_service'),


    # Toma un parámetro opcional llamado 'patent' compuesto por letras o números 
    # Esta ruta se usa para buscar una patente específica y está asociada al id de la cita o patente.
    re_path('search_patent/(?P<patent>[\w\d]+)?/', SearchPatentView.as_view(), name='search_patent'),



    # PATH para API (detalle vehiculos)  --test

    # path('obtener_marcas_y_modelos/', obtener_marcas_y_modelos, name='obtener_marcas_y_modelos'),
    # path('api/vehicle_data/', VehicleDataAPIView.as_view(), name='vehicle_data_api'),


    # path('get_models/<slug:brand_id>/', views.get_models, name='get_models'),
    # path('get_years/<int:model_id>/', views.get_years, name='get_years'),
    # path('get_models_choices/<slug:brand_slug>/', views.get_models_choices, name='get_models_choices'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
