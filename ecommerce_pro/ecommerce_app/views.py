from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,ProfileUpdateSerializer,ListUsersSerializer,ChangePasswordSerializer,ListAllProductsSerializer,CartItmesSerializer,OrderItemsSerializer,ReviewItemsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import NewUser,Product,CartItems,OrderItems,ReviewItems
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

#User API

class RegisterApiView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"MSG":"USER REGISTRAION COMPLETE!"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginApiView(APIView):
    def post(self,request):
        serializer  = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_token(user)
                return Response({"token":token,"msg":"Login Successful"},status=status.HTTP_200_OK)
            return Response({"msg":"email and password doesn't match"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = ProfileSerializer(instance=request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProfileUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def put(self,request):
        user = self.get_object()
        serializer = ProfileUpdateSerializer(user,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ListUserApiView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,request):
        user = NewUser.objects.all()
        serializer = ListUsersSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializers = ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializers.is_valid():
            return Response({"msg":"password change successfully"},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Products API

class ProductListApiView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ListAllProductsSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductByIdApiView(APIView):
    def get(self,request,id):
        product= get_object_or_404(Product,id=id)
        serializer = ListAllProductsSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductMakeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if not request.user.is_seller:
            raise PermissionError('For create a product u must be a seller')
        serializer = ListAllProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(seller = request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ProductUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None
    def put(self,request,id):
        product = self.get_object(id)
        if not product:
            return Response({"msg":"Product Not Found"},status=status.HTTP_404_NOT_FOUND)
        if product.seller != request.user:
            raise PermissionDenied("You don't have permmision to update this product")
        serializer = ListAllProductsSerializer(product,data=request.data,partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteProductApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None
        
    def delete(self,request,id):
        product = self.get_object(id)
        if not product:
            return Response({"msg":"Product Not Found"},status=status.HTTP_404_NOT_FOUND)
        if product.seller != request.user:
            raise PermissionDenied("You don't have permmision to delete this product")
        product.delete()
        return Response({"Details":"Product Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
    
#Cart API

class GetCartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        itmes = CartItems.objects.filter(user = request.user)
        serializer = CartItmesSerializer(itmes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AddProductToCartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity',1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = CartItems.objects.get_or_create(
            user = request.user,
            product = product,
            defaults= {'quantity':quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        serializer = CartItmesSerializer(cart_item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class cartUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,id):
        try:
            cart_item = CartItems.objects.get(id=id,user=request.user)
        except CartItems.DoesNotExist:
            return Response({"error":"Product Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartItmesSerializer(cart_item,data=request.data,partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCartItemApiView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        try:
            cart_item = CartItems.objects.get(id=id,user=request.user)
        except CartItems.DoesNotExist:
            return Response({"error":"Item Not Found"},status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Order Items Api

class OrderCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        cart_items = CartItems.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"msg":"Your Cart is Empty"},status=status.HTTP_400_BAD_REQUEST)
        
        order = OrderItems.objects.create(user=request.user)
        total_price = 0
        for item in cart_items:
            total_price += item.quantity*item.product.price
        order.total_price = total_price

        order.save()
        cart_items.delete()
        serializer = OrderItemsSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class ListAllOrderApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orders = OrderItems.objects.filter(user=request.user)
        serializer = OrderItemsSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ListAllOrderById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        try:
            order = OrderItems.objects.get(id=id,user=request.user)
        except OrderItems.DoesNotExist:
            return Response({"msg":"Order not Found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemsSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)

class OrderUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return OrderItems.objects.get(id=id)
        except OrderItems.DoesNotExist:
            return None
    
    def put(self,request,id):
        order = self.get_object(id=id)
        if order is None:
            return Response({"msg":"Order is not found"},status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff and order.user == request.user:
            raise PermissionDenied("You do not have a permission to update this order.")
        
        serializer = OrderItemsSerializer(order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Review item views

class MakeReviewAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get product_id from the request data
        product_id = request.data.get('product_id')  # Fetch product_id from the request data

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new review
        serializer = ReviewItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListOfReviews(APIView):
    def get(self,request):
        review = ReviewItems.objects.all()
        serializer = ReviewItemsSerializer(review,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ReviewUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, review_id, user):
        try:
            review = ReviewItems.objects.get(id=review_id, user=user)
            return review
        except ReviewItems.DoesNotExist:
            raise PermissionDenied("You do not have permission to update this review or the review doesn't exist.")

    def put(self, request, review_id):
        review = self.get_object(review_id, request.user)
        
        # Validate and update the review
        serializer = ReviewItemsSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, review_id, user):
        try:
            review = ReviewItems.objects.get(id=review_id, user=user)
            return review
        except ReviewItems.DoesNotExist:
            raise PermissionDenied("You do not have permission to delete this review.")

    def delete(self, request, review_id):
        review = self.get_object(review_id, request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)