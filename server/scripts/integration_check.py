import os,time,requests
base=os.getenv('TEST_BASE_URL','http://127.0.0.1:8000')
for attempt in range(30):
    try:
        response=requests.get(base+'/djangoapp/get_dealers',timeout=4)
        if response.status_code==200:break
    except requests.RequestException:pass
    time.sleep(1)
else:raise RuntimeError('Application services did not become ready')
dealers=response.json()['dealers'];assert len(dealers)==50
kansas=requests.get(base+'/djangoapp/get_dealers/Kansas',timeout=10).json()['dealers']
assert kansas and all(x['state']=='Kansas' for x in kansas)
reviews=requests.get(base+'/djangoapp/reviews/dealer/1',timeout=30).json()['reviews']
assert all(x['sentiment'] in ['positive','neutral','negative'] for x in reviews)
assert requests.get(base+'/djangoapp/get_cars').json()['CarModels']
assert requests.get(base+'/').status_code==200
print('PASS: 50 dealers, state filter, MongoDB reviews, sentiment integration, car catalogue, and frontend.')
