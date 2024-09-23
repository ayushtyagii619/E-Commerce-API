from django.urls import path,include
from .views import RegisterApiView,LoginApiView,ProfileApiView,ProfileUpdateApiView,ListUserApiView,ChangePasswordApiView,ProductListApiView,ProductByIdApiView,ProductMakeApiView,ProductUpdateApiView,DeleteProductApiView,GetCartApiView,AddProductToCartApiView,cartUpdateApiView,DeleteCartItemApiView,OrderCreateApiView,ListAllOrderApiView,ListAllOrderById,OrderUpdateApiView,MakeReviewAPiView,ListOfReviews,ReviewUpdateApiView,ReviewDeleteApiView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterApiView.as_view(),name='register'),
    path('login/',LoginApiView.as_view(),name='login'),
    path('profile/',ProfileApiView.as_view(),name='profile'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    path('update/',ProfileUpdateApiView.as_view(),name='update'),
    path('list-user/',ListUserApiView.as_view(),name='list_users'),
    path('change-password/',ChangePasswordApiView.as_view(),name='password_change'),
    path('products/',ProductListApiView.as_view(),name='products'),
    path('products/<int:id>/',ProductByIdApiView.as_view(),name='product_by_id'),
    path('product/',ProductMakeApiView.as_view(),name='new product'),
    path('product/<int:id>/',ProductUpdateApiView.as_view(),name='update product'),
    path('product/<int:id>/delete/',DeleteProductApiView.as_view(),name='delete product'),
    path('cart/',GetCartApiView.as_view(),name='get itmes'),
    path('cart/add/',AddProductToCartApiView.as_view(),name='new product'),
    path('cart/update/<int:id>/',cartUpdateApiView.as_view(),name='cart_update'),
    path('cart/delete/<int:id>/',DeleteCartItemApiView.as_view(),name='delete_item'),
    path('order/',OrderCreateApiView.as_view(),name='order-item'),
    path('orders/',ListAllOrderApiView.as_view(),name='order_list'),
    path('orders/<int:id>/',ListAllOrderById.as_view(),name='order_by_id'),
    path('orders/<int:id>/update/',OrderUpdateApiView.as_view(),name='order-update'),
    path('review/add/',MakeReviewAPiView.as_view(),name='add review'),
    path('reviews/',ListOfReviews.as_view(),name='list-reviews'),
    path('review/update/<int:review_id>/',ReviewUpdateApiView.as_view(),name='review-update'),
    path('review/delete/<int:review_id>/',ReviewDeleteApiView.as_view(),name='review-delete'),
]