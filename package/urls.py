from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('<uuid:uid>/', PackageView.as_view(), name="single_package_view"),
    path('types/', PackageTypeList.as_view(), name="list_package_types"),
    path('type/<uuid:uid>/', PackageListCategorized.as_view(), name="package_list_typed"),
    path('items/', PackageListUncategorized.as_view(), name="package_list_untyped"),
    path('img/',PackageImages.as_view(),name="package_image"),
    path('img/<uuid:uid>/',PackageImages.as_view(),name="list_package_Images"),
    path('hazards/',HarzardsView.as_view(),name="hazardLevel_view")
]
