from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from .models import UserProfile, Room, Approval, Fees
# Create your views here.
from .forms import UserProfileForm, ExtendedUserCreationForm, RoomCreationForm, UserUpdateForm, UserProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings


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
                       'gender': obj.gender, 'room': obj.room.no, 'email': obj.user.email,
                       'course': obj.course, 'fees': obj.fees_paid}
        except:
            context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                       'gender': obj.gender, 'room': 'Not Assigned', 'email': obj.user.email,
                       'course': obj.course, 'fees': obj.fees_paid}
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
            y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains, 'cover': x.cover}
            roomdata.append(y)
            print('hello', x.cover)
        context = {'roomdata': roomdata}
        return render(request, 'accounts/room_all.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required()
def room_change_view(request):
    # request.session['userred1'] = True
    rooms = Room.objects.all()
    obj = UserProfile.objects.get(user=request.user)
    roomdata = []
    for x in rooms:
        if x != obj.room:
            remains = x.capacity - x.present
            y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains, 'cover': x.cover}
            roomdata.append(y)

    context = {'roomdata': roomdata}
    return render(request, 'accounts/change_allrooms.html', context)


@login_required()
def room_change_check(request):
    current_user = request.user
    try:
        app = Approval.objects.get(requester__user__username=current_user)
        print(app)
        return render(request, 'accounts/room_notallowed.html')
    except:
        return room_change_view(request)


@login_required()
def room_all_view_warden(request):
    if request.user.groups.filter(name__in=['warden']).exists() == True:
        rooms = Room.objects.all()
        roomdata = []
        for x in rooms:
            remains = x.capacity - x.present
            y = {'no': x.no, 'type': x.room_type, 'present': x.present, 'remains': remains, 'cover': x.cover}
            roomdata.append(y)
            print(x.cover)
        context = {'roomdata': roomdata}
        return render(request, 'accounts/room_all_warden.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required()
def approve_all_view_warden(request):
    if request.user.groups.filter(name__in=['warden']).exists() == True:
        app = Approval.objects.all()
        appdata = []
        for x in app:
            if x.is_approved == False:
                y = {'old': x.old_room.no, 'new': x.new_room.no, 'user': x.requester.user.first_name,
                     'course': x.requester.course, 'username': x.requester}
                appdata.append(y)
                print(x)
        context = {'appdata': appdata}
        return render(request, 'accounts/approve_list.html', context)

    else:
        return render(request, 'accounts/testing.html')


def approve_confirm(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists() == True:

        # app = Approval.objects.get(id=tag)
        app = Approval.objects.filter(requester__user__username=tag).first()
        print('app is', app)
        user = UserProfile.objects.get(user__username=tag)
        oldroom = user.room
        oldroom.present = oldroom.present - 1
        newroom = app.new_room
        newroom.present = newroom.present + 1
        # Room additon problem
        user.room = newroom
        oldroom.save()
        newroom.save()
        user.save()
        app.delete()
        transaction.commit()

        subject = 'Your request has been approved'
        message = 'Your room change request has been approved by the warden. Login to see your new room.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.user.email]
        send_mail(subject, message, email_from, recipient_list)

        return approve_all_view_warden(request)

    else:
        return render(request, 'accounts/testing.html')


def approve_reject(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists() == True:

        # app = Approval.objects.get(id=tag)
        app = Approval.objects.filter(requester__user__username=tag).first()
        user = UserProfile.objects.get(user__username=tag)

        app.delete()
        transaction.commit()

        subject = 'Your request has been rejected'
        message = 'Your room change request has been rejected by the warden.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.user.email]
        send_mail(subject, message, email_from, recipient_list)

        return approve_all_view_warden(request)

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
def room_change(request, tag):
    # if 'userred1' in request.session:
    current_user = request.user
    print(current_user)
    obj = UserProfile.objects.get(user=current_user)
    req = Approval()
    req.requester = obj
    req.old_room = obj.room

    robj = Room.objects.get(no=tag)
    req.new_room = robj
    req.save()
    transaction.commit()
    # # print(obj.room.no)
    #
    #
    # # print(word)
    # robj = Room.objects.get(no=word)
    # print(robj.no)
    # robj.present = robj.present + 1
    # obj.room = robj
    # # print(obj.room.no)
    # obj.save()
    # robj.save()

    context = {'room': tag}
    return render(request, 'accounts/reqsent.html', context)

    # else:
    #     return render(request, 'accounts/testing.html')


@login_required()
def addroom(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST, request.FILES)

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
                l = {'name': x.user.first_name, 'username': x.user.username, 'room': x.room.no, 'course': x.course}
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


@login_required
def update(request):
    if request.method == 'POST':
        print('into first post')
        form = UserUpdateForm(request.POST)
        profile_form = UserProfileUpdateForm(request.POST)

        # if form.is_valid() and profile_form.is_valid():
        try:
            print('into validation')
            uname = request.POST['username']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            loc = request.POST['location']
            age1 = request.POST['age']
            user = User.objects.get(username=request.user)
            profile = UserProfile.objects.get(user=user)
            user.username = uname
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            profile.location = loc
            profile.age = age1
            profile.save()
            transaction.commit()
            return redirect('student')

        # else:
        except:
            # print('not valid')
            # return redirect('update')
            return render(request, 'accounts/update.html', {
                'form': form, 'form1': profile_form,
            })


    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        form = UserUpdateForm(instance=user)

        profile = UserProfile.objects.get(user=user)
        profile_form = UserProfileUpdateForm(instance=profile)

        return render(request, 'accounts/update.html', {
            'form': form, 'form1': profile_form,
        })


def fee_student_history(request):
    cuser = request.user
    print(cuser)
    allfees = Fees.objects.filter(student__user=cuser)
    details = []
    for x in allfees:
        l = {'name': x.student.user.first_name, 'date': x.date_paid}
        print(l)
        details.append(l)

    context = {'details': details}
    print(allfees)
    return render(request, 'accounts/feehistory.html', context)
