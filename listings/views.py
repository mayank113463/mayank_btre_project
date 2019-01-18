from django.shortcuts import render
#import data from model
from .models import Listing
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from  django.shortcuts import get_object_or_404
from .choices import state_choices,price_choices,bedroom_choices

# Create your views here.
def index(request):
    listings = Listing.objects.all().order_by('-list_date').filter(is_published=True)  #order by time shows first who create first
    #filter for admin area if i did not publish it than it should not show in area
    paginator = Paginator(listings,2) #2 contacts per page for listings
    page = request.GET.get('page')
    page_listings = paginator.get_page(page)
    context = {
        'listings': page_listings
    }
    return render(request, 'listings/listings.html',context)



def listing(request,listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    context = {
        'listing' : listing
    }
    return render(request,'listings/listing.html',context)
#here listing_id i have to mention because its comes with request as get



def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    #Keywords search-->
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    #City search
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
     # state search
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']   #here in braces its looking for the name which is written in form fiels of index page
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price) # name should be added in index page

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values' : request.GET
    }

    return render(request,'listings/search.html',context)