import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product , Contact , Orders , OrderUpdate
from math import ceil 
# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
   
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products} 
    # all_prods = [[products, range(1,nSlides),nSlides ], [products, range(1,nSlides),nSlides]]
    all_prods =[]
    catprods = Product.objects.values('category', 'id')
    # print(catprods)
    
    cat = {item['category'] for item in catprods}
    for cat in cat:
        # print(cat)
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        all_prods.append([prod,range(1, nSlides), nSlides])
        params = {'allProds':all_prods} 
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, "shop/about.html") 

def contact(request):
    thank = False 
    if request.method=="POST":
        # print("request is:")
        # print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        query = request.POST.get('query','')
        # print(name, email, query) 
        contact = Contact(name = name, email = email , query = query )
        contact.save()
        thank = True
    return render(request, "shop/contact.html", {'thank': thank})

# def tracker(request):
#     if request.method=="POST":
#         orderId = request.POST.get('orderId', '')
#         email = request.POST.get('email', '')
#         # print(orderId, email)
#         try:
#             order = Orders.objects.filter(order_id=orderId, email=email)
            
            
#             if len(order)>0:
#                 # print("order is",order)
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 print(OrderUpdate.objects.filter(order_id=orderId))
#                 # print("update is", update)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     # print(updates)
#                     response = json.dumps(updates, default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')
#         except Exception as e:
#             print("error")
#             print(e)
#             return HttpResponse('{}')

#     return render(request, 'shop/tracker.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def searchMatch(query, item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def prodView(request, myid):
    product = Product.objects.filter(id = myid)
    print(product)
    return render(request, "shop/prodView.html",{'product':product[0]}) 
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name,amount=amount, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')