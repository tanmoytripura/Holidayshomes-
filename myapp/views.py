from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import homedata
import pickle

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html', {'invalid_credentials': True}) 
        
    return render(request, 'login.html', {'invalid_credentials': False}) 


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        alluserlist = User.objects.all()
        chkul = []
        for i in alluserlist:
            chkul += [str(i)]
        if password1 == password2:
            if username not in chkul:
                User.objects.create_user(username=username, password=password1)
                return redirect('/user')
            else:
                messages.error(request, "Username already taken")
                return render(request, 'signin.html', {'invalid_credentials': 'Username already taken'}) 
        else:
            messages.error(request, "Password doesn't match")
            return render(request, 'signin.html', {'invalid_credentials': "Password doesn't match"}) 


    return render(request, 'signin.html', {'invalid_credentials': "False"})



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import homedata

@login_required
def user_page(request):
    username = request.user.username  # Get the logged-in user's username
    holiday_homes = homedata.objects.all()  # Fetch all holiday homes

    context = {
        'username': username,
        'holiday_homes': holiday_homes,
    }
    return render(request, 'user.html', context)


def logoutuser(request):
    logout(request)
    return redirect('/')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def keyword_recommendation(keyword, df, tfidf_matrix, tfidf):
    
    tfidf_matrix_keyword = tfidf.transform([keyword])

    cosine_sim = cosine_similarity(tfidf_matrix_keyword, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    home_indices = [i[0] for i in sim_scores[:5]] 

    return df.iloc[home_indices]

import numpy
def ai_recommendation(request):
    keyword = request.GET.get('keyword')
    recommended_homes = None

    if keyword:
        df = pickle.load(open('df.pkl','rb'))
        tfidf_matrix = pickle.load(open('mtx.pkl','rb'))
        tfidf = pickle.load(open('tfidf.pkl','rb'))
        recommended_homes = keyword_recommendation(keyword, df, tfidf_matrix, tfidf)
        recommended_homes = numpy.array(recommended_homes)
        recommended_homes = recommended_homes.tolist()
        print(recommended_homes)

    context = {
        'recommended_homes': recommended_homes,
        'keyword': keyword,
    }
    return render(request, 'ai.html', context)


def addtodata(request):
    pass
    global data
    for i in data:
        dbstore = homedata.objects.create(
            name=i['name'],
            location=i['location'],
            price=i['price_per_night'],  
            bedrooms=i['bedrooms'],  
            bathrooms=i['bathrooms'],  
            capacity=i['capacity'],  
            amenities=i['amenities'],  
            description=i['description'], 
        )
    return render(request, 'homepage.html')



data = [
    {
        "id": 1,
        "name": "Seaside Retreat",
        "location": "Malibu, CA",
        "price_per_night": 300,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Pool", "Beachfront", "Wi-Fi", "BBQ Grill"],
        "description": "A beautiful beachfront home with stunning ocean views and modern amenities.",
        "image_url": "https://example.com/images/seaside_retreat.jpg"
    },
    {
        "id": 2,
        "name": "Mountain Getaway",
        "location": "Aspen, CO",
        "price_per_night": 450,
        "bedrooms": 4,
        "bathrooms": 3,
        "capacity": 8,
        "amenities": ["Hot Tub", "Fireplace", "Ski-in/Ski-out", "Wi-Fi"],
        "description": "A luxurious mountain cabin perfect for winter sports enthusiasts.",
        "image_url": "https://example.com/images/mountain_getaway.jpg"
    },
    {
        "id": 3,
        "name": "Urban Oasis",
        "location": "New York, NY",
        "price_per_night": 200,
        "bedrooms": 2,
        "bathrooms": 1,
        "capacity": 4,
        "amenities": ["Gym", "Rooftop Terrace", "Wi-Fi", "Parking"],
        "description": "A stylish apartment located in the heart of the city with easy access to attractions.",
        "image_url": "https://example.com/images/urban_oasis.jpg"
    },
    {
        "id": 4,
        "name": "Lakeside Cabin",
        "location": "Lake Tahoe, NV",
        "price_per_night": 250,
        "bedrooms": 2,
        "bathrooms": 1,
        "capacity": 5,
        "amenities": ["Kayaks", "Fire Pit", "Wi-Fi", "Pet-Friendly"],
        "description": "A cozy cabin by the lake, perfect for summer adventures and winter retreats.",
        "image_url": "https://example.com/images/lakeside_cabin.jpg"
    },
    {
        "id": 5,
        "name": "Tropical Paradise",
        "location": "Kauai, HI",
        "price_per_night": 600,
        "bedrooms": 5,
        "bathrooms": 4,
        "capacity": 10,
        "amenities": ["Private Pool", "Ocean View", "Wi-Fi", "Chef Service"],
        "description": "An exquisite villa surrounded by lush landscapes and breathtaking views.",
        "image_url": "https://example.com/images/tropical_paradise.jpg"
    },
    {
        "id": 6,
        "name": "Countryside Cottage",
        "location": "Napa Valley, CA",
        "price_per_night": 180,
        "bedrooms": 2,
        "bathrooms": 1,
        "capacity": 4,
        "amenities": ["Wine Tasting", "Garden", "Wi-Fi", "Fireplace"],
        "description": "A charming cottage in the heart of wine country, perfect for a romantic getaway.",
        "image_url": "https://example.com/images/countryside_cottage.jpg"
    },
    {
        "id": 7,
        "name": "Desert Retreat",
        "location": "Palm Springs, CA",
        "price_per_night": 400,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Private Pool", "Hot Tub", "Wi-Fi", "Fire Pit"],
        "description": "A luxurious desert villa with breathtaking mountain views and a spacious outdoor area.",
        "image_url": "https://example.com/images/desert_retreat.jpg"
    },
    {
        "id": 8,
        "name": "Coastal Escape",
        "location": "Cape Cod, MA",
        "price_per_night": 350,
        "bedrooms": 4,
        "bathrooms": 3,
        "capacity": 8,
        "amenities": ["Beach Access", "Fireplace", "Wi-Fi", "BBQ Grill"],
        "description": "A charming coastal home perfect for family vacations and summer getaways.",
        "image_url": "https://example.com/images/coastal_escape.jpg"
    },
    {
        "id": 9,
        "name": "City View Apartment",
        "location": "San Francisco, CA",
        "price_per_night": 220,
        "bedrooms": 1,
        "bathrooms": 1,
        "capacity": 2,
        "amenities": ["Wi-Fi", "City View", "Parking", "Elevator"],
        "description": "An elegant apartment with stunning views of the San Francisco skyline.",
        "image_url": "https://example.com/images/city_view_apartment.jpg"
    },
    {
        "id": 10,
        "name": "Rustic Farmhouse",
        "location": "Amish Country, PA",
        "price_per_night": 200,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Farm Tour", "Garden", "Wi-Fi", "Pet-Friendly"],
        "description": "A cozy farmhouse surrounded by rolling hills and beautiful landscapes.",
        "image_url": "https://example.com/images/rustic_farmhouse.jpg"
    },
    {
        "id": 11,
        "name": "Chalet in the Alps",
        "location": "Zermatt, Switzerland",
        "price_per_night": 800,
        "bedrooms": 5,
        "bathrooms": 4,
        "capacity": 12,
        "amenities": ["Ski-in/Ski-out", "Sauna", "Wi-Fi", "Fireplace"],
        "description": "A luxurious chalet with breathtaking views of the Matterhorn and direct access to ski slopes.",
        "image_url": "https://example.com/images/chalet_in_the_alps.jpg"
    },
    {
        "id": 12,
        "name": "Historic Manor",
        "location": "Charleston, SC",
        "price_per_night": 300,
        "bedrooms": 4,
        "bathrooms": 3,
        "capacity": 8,
        "amenities": ["Historic Site", "Wi-Fi", "Garden", "Parking"],
        "description": "A beautifully restored historic manor in the heart of Charleston.",
        "image_url": "https://example.com/images/historic_manor.jpg"
    },
    {
        "id": 13,
        "name": "Secluded Retreat",
        "location": "Sedona, AZ",
        "price_per_night": 450,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Hot Tub", "Wi-Fi", "Hiking Trails", "Fireplace"],
        "description": "A serene retreat surrounded by stunning red rock formations.",
        "image_url": "https://example.com/images/secluded_retreat.jpg"
    },
    {
        "id": 14,
        "name": "Beachfront Paradise",
        "location": "Cancun, Mexico",
        "price_per_night": 700,
        "bedrooms": 5,
        "bathrooms": 4,
        "capacity": 10,
        "amenities": ["All-Inclusive", "Private Pool", "Beach Access", "Spa Services"],
        "description": "An all-inclusive beachfront villa with luxurious amenities and stunning ocean views.",
        "image_url": "https://example.com/images/beachfront_paradise.jpg"
    },
    {
        "id": 15,
        "name": "Villa Amore",
        "location": "Tuscany, Italy",
        "price_per_night": 600,
        "bedrooms": 4,
        "bathrooms": 3,
        "capacity": 8,
        "amenities": ["Wine Tasting", "Swimming Pool", "Wi-Fi", "Chef Service"],
        "description": "A beautiful villa in the heart of Tuscany, perfect for wine lovers.",
        "image_url": "https://example.com/images/villa_amore.jpg"
    },
    {
        "id": 16,
        "name": "Modern Loft",
        "location": "Toronto, Canada",
        "price_per_night": 220,
        "bedrooms": 2,
        "bathrooms": 1,
        "capacity": 4,
        "amenities": ["Wi-Fi", "Gym", "Parking", "Rooftop Terrace"],
        "description": "A sleek and modern loft in downtown Toronto, perfect for urban explorers.",
        "image_url": "https://example.com/images/modern_loft.jpg"
    },
    {
        "id": 17,
        "name": "Farmhouse Stay",
        "location": "Napa Valley, CA",
        "price_per_night": 250,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Wine Tours", "Garden", "Wi-Fi", "Fire Pit"],
        "description": "Experience country living in this charming farmhouse with beautiful vineyard views.",
        "image_url": "https://example.com/images/farmhouse_stay.jpg"
    },
    {
        "id": 18,
        "name": "Island Retreat",
        "location": "Bahamas",
        "price_per_night": 800,
        "bedrooms": 4,
        "bathrooms": 4,
        "capacity": 10,
        "amenities": ["Private Beach", "Infinity Pool", "Wi-Fi", "Butler Service"],
        "description": "A luxurious island retreat with breathtaking views and exclusive amenities.",
        "image_url": "https://example.com/images/island_retreat.jpg"
    },
    {
        "id": 19,
        "name": "Eco-Friendly Lodge",
        "location": "Costa Rica",
        "price_per_night": 300,
        "bedrooms": 3,
        "bathrooms": 2,
        "capacity": 6,
        "amenities": ["Organic Garden", "Wi-Fi", "Eco-Tours", "Hiking Trails"],
        "description": "A sustainable lodge in the heart of the rainforest, perfect for nature lovers.",
        "image_url": "https://example.com/images/eco_friendly_lodge.jpg"
    },
    {
        "id": 20,
        "name": "Ski Chalet",
        "location": "Whistler, Canada",
        "price_per_night": 500,
        "bedrooms": 5,
        "bathrooms": 4,
        "capacity": 12,
        "amenities": ["Ski-in/Ski-out", "Hot Tub", "Wi-Fi", "Fireplace"],
        "description": "A luxurious ski chalet with direct access to the slopes and stunning mountain views.",
        "image_url": "https://example.com/images/ski_chalet.jpg"
    }
]
