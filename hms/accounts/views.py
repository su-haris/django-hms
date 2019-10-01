from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect
from .models import UserProfile, Room
# Create your views here.
from .forms import UserProfileForm, ExtendedUserCreationForm, RoomCreationForm


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)

            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('student')

    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}

    return render(request, 'accounts/register.html', context)


def testing(request):
    return render(request, 'accounts/testing.html')


def student_details_view(request):
    current_user = request.user
    print(current_user)
    obj = UserProfile.objects.get(user=current_user)
    print(obj.user.first_name)
    print(obj.user.last_name)

    try:
        context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                   'gender': obj.gender, 'room': obj.room.no}
    except:
        context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                   'gender': obj.gender, 'room': 'Not Assigned'}

    # context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
    #            'gender': obj.gender, 'room': obj.room.no}

    return render(request, 'accounts/detail_view.html', context)


def room_all_view(request):
    rooms = Room.objects.all()
    roomdata = []
    for x in rooms:
        remains = x.capacity - x.present
        y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains}
        roomdata.append(y)
    context = {'roomdata': roomdata}
    return render(request, 'accounts/room_all.html', context)


def room_select(request, tag):
    current_user = request.user
    print(current_user)
    obj = UserProfile.objects.get(user=current_user)

    # print(obj.room.no)

    word = tag
    # print(word)
    robj = Room.objects.get(no=word)
    print(robj.no)
    robj.present = robj.present + 1
    obj.room = robj
    # print(obj.room.no)
    obj.save()
    robj.save()
    transaction.commit()
    return render(request, 'accounts/testing.html')


def addroom(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)

        if form.is_valid():
            room = form.save()

    else:
        form = RoomCreationForm()

    context = {'form': form}
    return render(request, 'accounts/add_room.html', context)
