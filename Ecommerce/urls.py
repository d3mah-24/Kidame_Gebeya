
from django.contrib import admin
from django.urls import include, path
from api.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),



    path('update/', updater, name="update"),


    path('recent_products/', recent_products, name="recent_products"),
    # path('products/<str:username>/', doss, name="products"),
    path('products', productss.as_view(), name="products"),
    path('detail/<int:idd>/',  detail, name="product_detail"),
    path('products_length', products_length, name="products_length"),
    path('products_search/<str:q>/', products_search, name="products_search"),


    path('cart_count/',  cart_count),

    path('cart/',  Carts.as_view()),
    path('post/',  Posts.as_view()),
    path('order/',  order.as_view()),
    path('cart/<int:pk>/',  Carts.as_view()),
    path('cart/<int:pk>/<int:item>/',  Carts.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^.*',
                        TemplateView.as_view(template_name='index.html'))]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
