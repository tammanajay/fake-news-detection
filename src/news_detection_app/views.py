import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import *
from .models import *
import joblib

# Load the vectorizer
vectorization_loaded = joblib.load('tfidf_vectorizer.pkl')
# Load the trained model
LR_loaded = joblib.load('trained_model.pkl')


def logout_view(request):
    logout(request)
    return redirect('home')

def index(request):
    return render(request, 'main.html')


def login(request):
    if request.method == 'POST':
        try:
            username= request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                auth_login(request,user)
            if user:
                return render(request, 'main.html')
        except Exception as e:
            print(e)
            messages.warning("Fill the details")

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)



def register(request):
    form = CreateUserForm()
    form2 = StudentForm()
    students = Viewer.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form2 = StudentForm(request.POST)
        if form.is_valid() and form2.is_valid():
            print("Form is valid")
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            g = User.objects.create_user(username=username, email=email, password=password1, is_staff=False)
            g.save()
            person = User.objects.all().last()
            print(person)
            name = form2.cleaned_data['name']
            # email = form2.cleaned_data['email']
            phone = form2.cleaned_data['phone']

            g = Viewer(user=person, name=username, email=email, phone=phone)
            # g = Viewer(user=person, name=name, phone=phone)
            try:
                g.save()
                print(g)
            except Exception as e:
                messages.error(request,e)
                page = 'Student Registration'
                context = {
                    'form': form,
                    'form2': form2,
                    'page': page,
                    'students': students,
                }
                return render(request, 'register_student.html', context)
            messages.success(request, 'Account was created for ' + name)
            return redirect('login')
    context = {
        'form': form,
        'form2': form2,
        'students': students,
    }
    return render(request, 'register_student.html', context)


def home(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            print(title,content)
            new_text = title +" "+ content


            # Transform the input (ensure it's inside a list)
            xv_new = vectorization_loaded.transform([new_text])  # Wrap in a list

            # Get prediction probabilities
            probabilities = LR_loaded.predict_proba(xv_new)

            # Print the predicted class and its confidence score
            # Predict using the loaded model
            y_predict = LR_loaded.predict(xv_new)
            predicted_class = y_predict[0]
            confidence = max(probabilities[0])  # Highest probability for the predicted class

            print(f"Predicted Class: {predicted_class}")
            print(f"Confidence Score: {confidence:.4f}")

            detected_news = ''

            if y_predict[0] == 0:
                print("News detected as - Fake")
                detected_news = 'Fake'
            else:
                print("News detected as - Real")
                detected_news = 'Real'
            print(request.user.username,'-- user')
            viewer = Viewer.objects.filter(user=request.user)[0]
            obj,ret =Article.objects.get_or_create(title=title,content=content,is_fake = not(bool(y_predict[0])),user=viewer )
            if y_predict[0] != 0:
                obj.is_published = True
                obj.date_published=datetime.date.today()
                obj.save()
                Admins.objects.get_or_create(
                    article=obj,
                    user=request.user,
                    is_published=True,
                    is_reported=False,
                    updated_date=datetime.date.today(),
                    description='Detected as Real'
                )
            FakeDetection.objects.get_or_create(article=obj,is_fake=not(bool(y_predict[0])),confidence=confidence)

            articles = Article.objects.filter(is_fake__in=[False,None], is_published=True).order_by('-date_published')
            return render(request, 'result.html',{'output':detected_news,'articles':articles})
    else:
        form = NewsForm()
    return render(request, 'upload.html', {'form': form})



def article_list(request):
    fake_list = [False,None]
    articles = Article.objects.filter(is_fake__in=fake_list,is_published=True).order_by('-id')
    print(articles,'--- art')
    return render(request, 'news.html',{'articles':articles})



def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Get the article or return 404
    return render(request, "single_news.html", {"article": article})  # Pass to template