from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('blog',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('validate_otp/',views.validate_otp,name='validate_otp'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('update_password/',views.update_password,name='update_password'),
    path('change_password/',views.change_password,name='change_password'),
    path('profile/',views.profile,name='profile'),
    path('seller_index/',views.seller_index,name='seller_index'),
    
    path('add_gold_jewelry/',views.add_gold_jewelry,name='add_gold_jewelry'),
    
    path('view_gold_rings/',views.view_gold_rings,name='view_gold_rings'),
    path('view_gold_necklace/',views.view_gold_necklace,name='view_gold_necklace'),
    path('view_gold_earrings/',views.view_gold_earrings,name='view_gold_earrings'),
    path('view_gold_pendants/',views.view_gold_pendants,name='view_gold_pendants'),
    path('view_gold_bangles/',views.view_gold_bangles,name='view_gold_bangles'),
    path('view_gold_bracelet/',views.view_gold_bracelet,name='view_gold_bracelet'),
    path('view_gold_chains/',views.view_gold_chains,name='view_gold_chains'),
    
    path('gold_product_detail/<int:pk>/,',views.gold_product_detail,name='gold_product_detail'),
    path('gold_stock_availability/<int:pk>/',views.gold_stock_availability,name='gold_stock_availability'),
    path('edit_gold_jewelry/<int:pk>/',views.edit_gold_jewelry,name='edit_gold_jewelry'),    
    path('delete_gold_jewelry/<int:pk>/',views.delete_gold_jewelry,name='delete_gold_jewelry'),

    path('user_view_gold_jew/<str:gj>/',views.user_view_gold_jew,name='user_view_gold_jew'),
    path('user_gold_product_detail/<int:pk>/',views.user_gold_product_detail,name='user_gold_product_detail'),

    path('add_diamond_jewelry',views.add_diamond_jewelry,name='add_diamond_jewelry'),
        
    path('view_diamond_rings/',views.view_diamond_rings,name='view_diamond_rings'),
    path('view_diamond_necklace/',views.view_diamond_necklace,name='view_diamond_necklace'),
    path('view_diamond_earrings/',views.view_diamond_earrings,name='view_diamond_earrings'),
    path('view_diamond_pendants/',views.view_diamond_pendants,name='view_diamond_pendants'),
    path('view_diamond_bangles/',views.view_diamond_bangles,name='view_diamond_bangles'),
    path('view_diamond_bracelet/',views.view_diamond_bracelet,name='view_diamond_bracelet'),
    
    path('diamond_product_detail/<int:pk>/,',views.diamond_product_detail,name='diamond_product_detail'),
    path('diamond_stock_availability/<int:pk>/',views.diamond_stock_availability,name='diamond_stock_availability'),
    path('edit_diamond_jewelry/<int:pk>/',views.edit_diamond_jewelry,name='edit_diamond_jewelry'),    
    path('delete_diamond_jewelry/<int:pk>/',views.delete_diamond_jewelry,name='delete_diamond_jewelry'),

    path('user_view_diamond_jew/<str:dj>/',views.user_view_diamond_jew,name='user_view_diamond_jew'),
    path('user_diamond_product_detail/<int:pk>/',views.user_diamond_product_detail,name='user_diamond_product_detail'),

    path('add_platinum_jewelry/',views.add_platinum_jewelry,name='add_platinum_jewelry'),
    
    path('view_platinum_rings/',views.view_platinum_rings,name='view_platinum_rings'),
    path('view_platinum_necklace/',views.view_platinum_necklace,name='view_platinum_necklace'),
    path('view_platinum_earrings/',views.view_platinum_earrings,name='view_platinum_earrings'),
    path('view_platinum_pendants/',views.view_platinum_pendants,name='view_platinum_pendants'),
    path('view_platinum_bracelet/',views.view_platinum_bracelet,name='view_platinum_bracelet'),
    path('view_platinum_chains/',views.view_platinum_chains,name='view_platinum_chains'),
      
    path('platinum_product_detail/<int:pk>/,',views.platinum_product_detail,name='platinum_product_detail'),
    path('platinum_stock_availability/<int:pk>/',views.platinum_stock_availability,name='platinum_stock_availability'),
    path('edit_platinum_jewelry/<int:pk>/',views.edit_platinum_jewelry,name='edit_platinum_jewelry'),    
    path('delete_platinum_jewelry/<int:pk>/',views.delete_platinum_jewelry,name='delete_platinum_jewelry'),

    path('user_view_platinum_jew/<str:pj>/',views.user_view_platinum_jew,name='user_view_platinum_jew'),
    path('user_platinum_product_detail/<int:pk>/',views.user_platinum_product_detail,name='user_platinum_product_detail'),
    
    path('add_to_wishlist/<int:pk>/<str:a>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('move_to_wishlist/<int:pk>/<str:e>/',views.move_to_wishlist,name='move_to_wishlist'),
    path('remove_from_wishlist/<int:pk>/<str:c>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('mywishlist/',views.mywishlist,name='mywishlist'),

    path('add_to_cart/<int:pk>/<str:b>/',views.add_to_cart,name='add_to_cart'),
    path('move_to_cart/<int:pk>/<str:f>/',views.move_to_cart,name='move_to_cart'),
    path('remove_from_cart/<int:pk>/<str:d>/',views.remove_from_cart,name='remove_from_cart'),
    path('mycart/',views.mycart,name='mycart'),

    path('update_price/',views.update_price,name='update_price'),

    path('pay/',views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),
]   