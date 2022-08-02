from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as login_user, logout as logout_user
from .models import StocksModel, UserQueryModel
# import Q 
from django.db.models import Q
# login required decorator import
from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(View):
    
    
    def get(self, request, slug=None):
        if request.user.is_authenticated: 
            queries = UserQueryModel.objects.filter(user=self.request.user).order_by('-timestamp')

            if slug == 'next':
                # in order to get the stock data i'm adding the 5 to the slicing
                context = {
                    'stocks': StocksModel.objects.all()[ 0+5 : 5+5 ],
                    'queries': queries,
                }
                template_name = 'stocks/index.html'
                return render(request, template_name, context)
            
            else:

                context = {
                    'stocks': StocksModel.objects.all()[0:5],
                    'queries': queries,
                }
                template_name = 'stocks/index.html'
                return render(request, template_name, context)

        else:
            return render(request, 'stocks/index.html')

    def post(self,request, id=None, slug=None):
        if request.user.is_authenticated:
            print('saved !')
            stock_name = request.POST.get('stock_name')
            query = request.POST.get('message')
            user_ = request.user

            stock = StocksModel.objects.get(stock_name=stock_name)
            
            user_query = UserQueryModel(user=user_, stocks=stock, query=query)
            user_query.save()
            messages.success(request, 'Your query has been saved!')
            return redirect('/')
    

class RegisterView(View):
    def get(self, request):
        print('in get')
        return JsonResponse({'success': False})
    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are successfully registered and logged in!')
                return JsonResponse(status=200, data={'success': True})
            else:
                messages.error(request, 'Registration failed')
                return JsonResponse(staus=400, data={'success': False})

        else:
            messages.error(request, 'Your passwords do not match')
            return JsonResponse(staus=402, data={'success': False})


def login_view(request):
    method = request.method
    
    if method == 'GET':
        return render(request, 'stocks/login.html')

    elif method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password=password)
        if user is not None:
            login_user(request, user)
            messages.success(request, 'You are successfully logged in!')
            return redirect('/')
        else:
            messages.error(request, 'Login failed')
            return redirect('/login')

def logout_view(request):
    logout_user(request)
    return redirect('/')

@login_required(login_url='/login-user')
def search(request, pk=None):
    if request.user.is_authenticated:
        if pk is not None:
            if request.method == 'GET':

                stock_id = pk
                stock = StocksModel.objects.get(id=stock_id)
                queries = UserQueryModel.objects.filter(Q(user=request.user) & Q(stocks=stock))
                context = {
                    'stocks': stock,
                    'queries': queries,
                }
                template_name = 'stocks/search.html'
                return render(request, template_name, context)

            if request.method == 'POST':
                query = request.POST.get('message')
                user_ = request.user

                stock = StocksModel.objects.get(id=pk)
                user_query = UserQueryModel(user=user_, stocks=stock, query=query)
                user_query.save()

                messages.success(request, 'Your query has been saved!')
                return redirect('/search/'+str(pk))
            
        elif request.method == 'GET':
            try:
                stock_name = request.GET.get('search-text')
                stock = StocksModel.objects.get(stock_name__icontains=stock_name)
                queries = UserQueryModel.objects.filter(Q(user=request.user) & Q(stocks=stock))

                context = {
                    'stocks': stock,
                    'queries': queries,
                }

                template_name = 'stocks/search.html'
                return render(request, template_name, context)
            except:
                messages.error(request, 'No stock found')
                return redirect('/')

        else:
            messages.info(request, "Didn't find any stock with that name")
            return redirect('/')
    else:
        return redirect('/')

