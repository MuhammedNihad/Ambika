from django.urls import path
from . import views
from django.urls import path


urlpatterns = [
     path('', views.all_products, name='all_products'),
     path('create',views.create_product,name="create"),
     path('product/<int:product_id>/', views.single_product, name='single_product'),
       path('cart/', views.cart, name='cart'),
     path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
     path('update_addon/', views.update_addon, name='udpate_addon'),
       path('update_quantity/', views.update_quantity, name='update_quantity'),
        path('cart/<str:action>/', views.cart, name='cart'),
         path('place_order/', views.place_order, name='place_order'),
          path('placed_orders/', views.placed_orders, name='placed-orders'),
]