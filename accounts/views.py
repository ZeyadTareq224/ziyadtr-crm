from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
	
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
	'total_customers': total_customers,
	'customers': customers,
	'orders': orders,
	'total_orders': total_orders,
	'delivered': delivered,
	'pending': pending,
	}
	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

	products = Product.objects.all()

	context = {'products': products}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()

	myFilter = OrderFilter(request.GET, orders)
	orders = myFilter.qs 

	context = {
	'myFilter': myFilter,
	'customer': customer,
	'orders': orders
	}
	return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
	customer = Customer.objects.get(id=pk)
	form = OrderForm()
	
	if request.method == 'POST':
		form=OrderForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('home')
	context = {
	'form': form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('home')
	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('home')
	context = {'order': order}
	return render(request, 'accounts/delete_order.html', context)


@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			

			messages.success(request, 'Account Created Successfully')
			return redirect('login')
	context = {'form': form}
	return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):	
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, "Username Or Password Is Incorrect")
	context = {}
	return render(request, 'accounts/login.html', context)	


def logoutUser(request):
	logout(request)
	return redirect('login')	


def userPage(request):
	
	orders=request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
	'orders':orders,
	'total_orders':total_orders,
	'delivered':delivered,
	'pending':pending
	}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == "POST":
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('account')

	context = {'form': form}
	return render(request, 'accounts/account_settings.html', context)	