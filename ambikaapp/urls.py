from django.urls import path
from . import views
from django.urls import path


urlpatterns = [
     path('', views.all_products, name='all_products'),
     path('create',views.create_product,name="create"),
     path('product/<int:product_id>/', views.single_product, name='single_product'),
       path('cart/', views.cart, name='cart'),
     path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
       path('update_quantity/', views.update_quantity, name='update_quantity'),
        path('cart/<str:action>/', views.cart, name='cart'),
         path('place_order/', views.place_order, name='place_order'),
          path('placed_orders/', views.placed_orders, name='placed-orders'),
           path('sendsms/', views.sendsms, name='sendsms'),
          path('blog/',views.blog,name='blog'),
          path('blog_detail/<int:post_id>/', views.blog_detail, name='blog_detail'),
          path('phone_verification/', views.send_sms_verification, name='send_sms_verification'),
           path('trending/', views.trending_page, name='trending-page'),
]