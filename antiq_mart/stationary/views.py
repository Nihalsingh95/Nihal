from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Customer,Antique,Order,Cart
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm,CustomerForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class Furniture_Cart(View):
    def get(self,request):
        antique_category = Antique.objects.filter(category='FURNITURE')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'furniture_cart.html',{'antique_category':antique_category})

class Art_Cart(View):
    def get(self,request):
        antique_category = Antique.objects.filter(category='ART')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'art_cart.html',{'antique_category':antique_category})
    
class Instrument_Cart(View):
    def get(self,request):
        antique_category = Antique.objects.filter(category='INSTRUMENT')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'instrument_cart.html',{'antique_category':antique_category})
    
class Contact(View):
    def get(self,request):
        contact = Antique.objects.filter(category='contact')  # we are using filter function of queryset, that will filter those data whose category belongs to dog
        return render(request,'contact.html',{'contact':contact})



def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                return redirect('registration')    
        else:
            mf  = RegistrationForm()
        return render(request,'registration.html',{'mf':mf})
    else:
        return redirect('profile')

def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login ,if so it will show login option
        if request.method == 'POST':       # otherwise it will redirect to the profile page 
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'login.html',{'mf':mf})
    else:
        return redirect('profile')
    
def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'profile.html',{'name':request.user,'mf':mf})
    else:                                                # request.user returns the username
        return redirect('login')


def log_out(request):
    logout(request)
    return redirect('home')

def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'changepassword.html',{'mf':mf})
    else:
        return redirect('login')
    
def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'changepassword.html',{'mf':mf})
    else:
        return redirect('login')
    
class AntiqueDetailView(View):
    def get(self,request,id):     # id = It will fetch id of particular pet 
        antique = Antique.objects.get(pk=id)

        #------ code for caculate percentage -----
        if antique.discounted_price !=0:    # fetch discount price of particular pet
            percentage = int(((antique.selling_price-antique.discounted_price)/antique.selling_price)*100)
        else:
            percentage = 0
        # ------ code end for caculate percentage ---------
            
        return render(request,'antique_details.html',{'antique':antique,'percentage':percentage})


def add_to_cart(request, id):    # This 'id' is coming from 'pet.id' which hold the id of current pet , which is passing through {% url 'addtocart' pet.id %} from pet_detail.html 
    if request.user.is_authenticated:
        product = Antique.objects.get(pk=id) # product variable is holding data of current object which is passed through 'id' from parameter
        user=request.user                # user variable store the current user i.e steveroger
        Cart(user=user,product=product).save()  # In cart model current user i.e steveroger will save in user variable and current pet object will be save in product variable
        return redirect('antiquedetails', id)       # finally it will redirect to pet_details.html with current object 'id' to display pet after adding to the cart
    else:
        return redirect('login')                # If user is not login it will redirect to login page

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =100
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    return render(request, 'view_cart.html', {'cart_items': cart_items,'total':total,'final_price':final_price})

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity += 1                       # If object found it will be add 1 quantity to the current object   
    product.save()
    return redirect('viewcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save() 
    return redirect('viewcart')

def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')


def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            print('mf',mf)
            if mf.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                print(state)
                print(city)
                print(name)
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'mf':mf,'address':address})


def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =150
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)
