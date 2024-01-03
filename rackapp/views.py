from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
class CustRegistrationView(generics.CreateAPIView):
   
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = self.perform_create(serializer)
        return Response({'user_id': customer.user.id, 'username': customer.user.username, 'email': customer.user.email}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #  app_user = request.user.appuser
        #  serializer = AppUserSerializer(app_user)
        #  return Response(serializer.data)
        app_user = AppUser.objects.get(user=request.user)
        serializer = CombinedSerializer(app_user)
        return Response(serializer.data)
        # if request.user.is_authenticated:
        #     try:
        #         my_user = User.objects.get(user=request.user)
        #         serializer = UserSerializer(my_user)
        #         return Response(serializer.data)
        #     except User.DoesNotExist:
        #         return Response({'error': 'User instance not found'}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):       
        request.auth.delete()  
        
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

    
@api_view(['GET'])
def category_list(request):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response( serializer.data, status=status.HTTP_200_OK)

class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pro_id, **kwargs):
        product_obj = get_object_or_404(Product, id=pro_id)          
        cart_id = request.session.get("cart_id", None)             
        if cart_id:
            cart_obj = get_object_or_404(Cart, id=cart_id)
            
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0,)
            request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
            cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()        
        serializer = CartProductSerializer(cartproduct)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class MyCartView(APIView):
    
    def get(self, request,):
        context = {}        
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(cart)
        else:
            cart = None        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class ManageCartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cp_id = kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = get_object_or_404(CartProduct, id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return Response({"detail": "Action completed"}, status=status.HTTP_200_OK)
