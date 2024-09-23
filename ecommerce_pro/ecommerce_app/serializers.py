from rest_framework import serializers
from .models import NewUser,Product,ProductImage,CartItems,OrderItems,ReviewItems
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#user serializers

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
                                   validators = [UniqueValidator(queryset=NewUser.objects.all())]
                                   )
    password = serializers.CharField(write_only = True,required = True,validators = [validate_password])
    password2 = serializers.CharField(write_only = True,required = True)

    class Meta:
        model = NewUser
        fields = ['email','password','password2','name','mobile','address',]
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"password field didn't match"})
        return attrs
    def create(self,validate_data):
        user = NewUser.objects.create(
            email = validate_data['email'],
            name = validate_data['name'],
            mobile = validate_data['mobile'],
            address = validate_data['address'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=200)
    class Meta:
        model = NewUser
        fields = ['email','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','email','name','mobile','address']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['name','mobile','address']
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.mobile = validated_data.get('mobile',instance.name)
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance
    
class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','email','name','mobile','address','is_active']

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100,write_only=True,style = {'input_type':'password'})
    password2 = serializers.CharField(max_length = 100, write_only=True,style = {'input_type':'password'})
    class Meta:
        model = NewUser
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
    
#product serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']

class ListAllProductsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','description','price','quantity','seller','date_added','images']

#Cart Itmes Serializer

class CartItmesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['id','user','product','quantity','added_at']
        read_only_fields = ['id','user','added_at']

#order items serializer

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id','user','total_price','status','placed_at','updated_at']
        read_only_fields = ['id','user','total_price','placed_at','updated_at']

#Review Item

class ReviewItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewItems
        fields = ['id','product','user','rating','comment','created_at']
        read_only_fields = ['id','user','created_at']