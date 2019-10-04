from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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


@login_required()
def student_details_view(request):
    current_user = request.user
    print(current_user)

    if request.user.groups.filter(name__in=['warden']).exists() == True:
        return room_all_view_warden(request)

    else:
        obj = UserProfile.objects.get(user=current_user)
        print(obj.user.first_name)
        print(obj.user.last_name)

        try:
            context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                       'gender': obj.gender, 'room': obj.room.no}
        except:
            context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                       'gender': obj.gender, 'room': 'Not Assigned'}
            if request.user.is_authenticated and request.user.is_active:
                request.session['userred'] = True

        # context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
        #            'gender': obj.gender, 'room': obj.room.no}

        return render(request, 'accounts/detail_view.html', context)


@login_required()
def room_all_view(request):
    if 'userred' in request.session:
            request.session['userred1'] = True
            rooms = Room.objects.all()
            roomdata = []
            for x in rooms:
                remains = x.capacity - x.present
                y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains}
                roomdata.append(y)
            context = {'roomdata': roomdata}
            return render(request, 'accounts/room_all.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required()
def room_all_view_warden(request):
    if request.user.groups.filter(name__in=['warden']).exists() == True:
        rooms = Room.objects.all()
        roomdata = []
        for x in rooms:
            remains = x.capacity - x.present
            y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains}
            roomdata.append(y)
        context = {'roomdata': roomdata}
        return render(request, 'accounts/room_all_warden.html', context)

    else:
        return render(request, 'accounts/testing.html')



@login_required()
def room_select(request, tag):
    # if 'userred1' in request.session:
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
    context = {'room': tag}
    return render(request, 'accounts/confirm.html', context)

    # else:
    #     return render(request, 'accounts/testing.html')


@login_required()
def addroom(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)

        if form.is_valid():
            room = form.save()
            return student_details_view(request)

    else:
        form = RoomCreationForm()

    context = {'form': form}
    return render(request, 'accounts/add_room.html', context)


@login_required()
def room_details(request, tag):
    studs = UserProfile.objects.all()
    studdata = []
    rm = str(tag)
    print(studs[1].room.no)
    print(rm)
    for x in studs:
        try:
            y = x.room.no
            if y == rm:
                l = {'name': x.user.first_name, 'username': x.user.username, 'room': x.room.no}
                print(l)
                studdata.append(l)
        except:
            print('error')

    context = {'studdata': studdata, 'room': tag}
    print(context)
    return render(request, 'accounts/room_stud.html', context)


def landing(request):
    if request.user.is_authenticated:
        return student_details_view(request)

    else:
        return render(request, 'accounts/landing.html')
