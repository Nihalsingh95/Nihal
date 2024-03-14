from django.urls import path 
from .import views 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),

    path('contact/',views.Contact.as_view(),name='contact'),

    path('furniturecart/',views.Furniture_Cart.as_view(),name='furniturecart'),

    path('artcart',views.Art_Cart.as_view(),name='artcart'),

    path('instrument/',views.Instrument_Cart.as_view(),name='instrumentcart'),

    path('registration/',views.registration,name='registration'),

    path('login/',views.log_in,name='login'),

    path('profile/',views.profile,name='profile'),

    path('address/',views.address,name='address'),

    path('logout/',views.log_out, name="logout"),

    path('changepassword/',views.changepassword, name="changepassword"),
    path('antique_details/<int:id>/',views.AntiqueDetailView.as_view(),name='antiquedetails'),

    path('add_to_cart/<int:id>/',views.add_to_cart, name="addtocart"),

    path('view_cart/',views.view_cart, name="viewcart"),

    path('add_quantity/<int:id>/', views.add_quantity, name='add_quantity'),

    path('delete_quantity/<int:id>/', views.delete_quantity, name='delete_quantity'),

    path('delete_cart/<int:id>',views.delete_cart, name="deletecart"),

    path('about',views.about,name='about'),

    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),

    path('checkout/',views.checkout,name='checkout'),

   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)