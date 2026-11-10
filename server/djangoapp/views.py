import json
from datetime import date
from functools import wraps
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET
from .models import CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

def guarded(fn):
    @wraps(fn)
    def view(request,*args,**kwargs):
        try:return fn(request,*args,**kwargs)
        except (ValueError,KeyError,TypeError,ValidationError):return JsonResponse({'error':'Invalid input'},status=400)
        except requests.RequestException:return JsonResponse({'error':'A supporting service is unavailable'},status=503)
    return view
@require_GET
@ensure_csrf_cookie
def csrf(request):return JsonResponse({'csrfToken':get_token(request)})
@require_GET
def session(request):return JsonResponse({'userName':request.user.username if request.user.is_authenticated else None})
@require_POST
@guarded
def login_user(request):
    data=json.loads(request.body);user=authenticate(request,username=data['userName'],password=data['password'])
    if user is None:return JsonResponse({'error':'Invalid username or password'},status=401)
    login(request,user);return JsonResponse({'userName':user.username,'status':'Authenticated'})
@require_POST
def logout_request(request):
    logout(request);return JsonResponse({'status':'Logged out'})
@require_POST
@guarded
def registration(request):
    data=json.loads(request.body);username=data['userName'].strip()
    if not username or len(username)>150:raise ValueError('username')
    validate_password(data['password'])
    try:
        with transaction.atomic():
            user=User.objects.create_user(username=username,password=data['password'],email=data.get('email',''),first_name=data.get('firstName',''),last_name=data.get('lastName',''))
    except IntegrityError:return JsonResponse({'error':'This username is already registered'},status=409)
    login(request,user);return JsonResponse({'status':'Authenticated','userName':user.username},status=201)
@require_GET
@guarded
def get_dealerships(request,state='All'):
    from urllib.parse import quote
    return JsonResponse({'status':200,'dealers':get_request('fetchDealers/'+quote(state,safe=''))})
@require_GET
@guarded
def get_dealer_details(request,dealer_id):return JsonResponse({'status':200,'dealer':get_request(f'fetchDealer/{dealer_id}')})
@require_GET
@guarded
def get_dealer_reviews(request,dealer_id):
    reviews=get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:review['sentiment']=analyze_review_sentiments(review['review'])
    return JsonResponse({'status':200,'reviews':reviews})
@require_GET
def get_cars(request):
    return JsonResponse({'CarModels':[{'id':c.pk,'CarMake':c.car_make.name,'CarModel':c.name,'year':c.year} for c in CarModel.objects.select_related('car_make').all()]})
@require_POST
@guarded
def add_review(request):
    if not request.user.is_authenticated:return JsonResponse({'error':'Sign in to post a review'},status=401)
    data=json.loads(request.body)
    car=CarModel.objects.select_related('car_make').filter(pk=data['car_id']).first()
    if car is None:raise ValueError('car')
    when=date.fromisoformat(data['purchase_date'])
    if when>date.today() or not str(data['review']).strip() or len(data['review'])>5000:raise ValueError('review')
    payload={'name':request.user.get_full_name() or request.user.username,'dealership':int(data['dealership']),'review':data['review'],'purchase':True,'purchase_date':when.isoformat(),'car_make':car.car_make.name,'car_model':car.name,'car_year':car.year}
    result=post_review(payload);return JsonResponse({'status':200,'review':result},status=201)
