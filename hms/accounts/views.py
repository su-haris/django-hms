from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import UserProfile, Room, Approval, Fees, NewRegistration
# Create your views here.
from .forms import UserProfileForm, ExtendedUserCreationForm, RoomCreationForm, UserUpdateForm, UserProfileUpdateForm, \
    RejectForm
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
            context = {'form': form, 'profile_form': profile_form}
            return render(request, 'accounts/register.html', context)

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

    if request.user.groups.filter(name__in=['warden']).exists():
        return redirect('wardenhome')

    elif request.user.is_superuser:
        return render(request, 'accounts/testing2.html')

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
        try:
            s = NewRegistration.objects.get(requester__user__username=request.user)
            print(s, 'hello')
            return render(request, 'accounts/room_notallowed.html')
        except:
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
    if request.user.groups.filter(name__in=['warden']).exists():
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
    if request.user.groups.filter(name__in=['warden']).exists():
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


@login_required()
def new_approve_all_view_warden(request):
    if request.user.groups.filter(name__in=['warden']).exists():
        app = NewRegistration.objects.all()
        appdata = []
        for x in app:
            y = {'new': x.new_room.no, 'user': x.requester.user.first_name, 'userl': x.requester.user.last_name,
                 'course': x.requester.course, 'username': x.requester}
            appdata.append(y)
            print(x)
        context = {'appdata': appdata}
        return render(request, 'accounts/approve_list_new.html', context)

    else:
        return render(request, 'accounts/testing.html')


def reject_form(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        if request.method == 'POST':
            form = RejectForm(request.POST)

            if form.is_valid():
                # msg = request.POST['message']
                msg = request.POST.get('message')
                print(msg)
                app = NewRegistration.objects.filter(requester__user__username=tag).first()
                user = UserProfile.objects.get(user__username=tag)
                subject = 'Your request has been rejected'
                message = 'Your new room selection has been rejected by the warden.' \
                          'Reason: '
                message = message + msg
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.user.email]
                send_mail(subject, message, email_from, recipient_list)
                app.delete()
                return redirect('applistnew')

            else:
                form = RejectForm()
                return render(request, 'accounts/reject_msg_new.html', {'form': form, 'username': tag})

        else:
            form = RejectForm()
            return render(request, 'accounts/reject_msg_new.html', {'form': form, 'username': tag})


def approve_confirm_new(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        # app = Approval.objects.get(id=tag)
        app = NewRegistration.objects.filter(requester__user__username=tag).first()
        print('app is', app)
        user = UserProfile.objects.get(user__username=tag)
        newroom = app.new_room
        if newroom.present == newroom.capacity:
            app.delete()
            transaction.commit()
            subject = 'Your request has been cancelled'
            message = 'Your room change request has been cancelled by the warden because the room was already full' \
                      ' at the time of processing.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.user.email]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'accounts/room_full.html')

        else:
            newroom.present = newroom.present + 1
            user.room = newroom
            newroom.save()
            user.save()
            app.delete()
            transaction.commit()

            subject = 'Your request has been approved'
            message = 'Your new room request has been approved by the warden. Login to see your new room.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.user.email]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('applist')

    else:
        return render(request, 'accounts/testing.html')


def approve_confirm(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        # app = Approval.objects.get(id=tag)
        app = Approval.objects.filter(requester__user__username=tag).first()
        print('app is', app)
        user = UserProfile.objects.get(user__username=tag)
        oldroom = user.room
        newroom = app.new_room
        if newroom.present == newroom.capacity:
            app.delete()
            transaction.commit()
            subject = 'Your request has been cancelled'
            message = 'Your room change request has been cancelled by the warden because the room was already full' \
                      ' at the time of processing.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.user.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('applist')

        else:
            oldroom.present = oldroom.present - 1
            newroom.present = newroom.present + 1
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

            return redirect('applist')

    else:
        return render(request, 'accounts/testing.html')


def approve_reject(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        if request.method == 'POST':
            form = RejectForm(request.POST)

            if form.is_valid():
                # msg = request.POST['message']
                msg = request.POST.get('message')
                # app = Approval.objects.get(id=tag)
                app = Approval.objects.filter(requester__user__username=tag).first()
                user = UserProfile.objects.get(user__username=tag)

                subject = 'Your request has been rejected'
                message = 'Your room change request has been rejected by the warden. Reason:'
                message = message + msg
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.user.email]
                send_mail(subject, message, email_from, recipient_list)

                app.delete()
                transaction.commit()

                return approve_all_view_warden(request)

            else:
                form = RejectForm()
                return render(request, 'accounts/reject_msg_change.html', {'form': form, 'username': tag})

        else:
            form = RejectForm()
            return render(request, 'accounts/reject_msg_change.html', {'form': form, 'username': tag})

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


def room_select_new(request, tag):
    try:
        s = NewRegistration.objects.get(requester__user__username=request.user)
        print(s, 'hello')
        return render(request, 'accounts/room_notallowed.html')
    except:
        current_user = request.user
        print(current_user)
        obj = UserProfile.objects.get(user=current_user)

        room = NewRegistration()
        room.requester = obj
        room.new_room = Room.objects.get(no=tag)
        room.save()
        context = {'room': tag}
        return render(request, 'accounts/confirm.html', context)


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
    if request.user.groups.filter(name__in=['warden']).exists():
        if request.method == 'POST':
            form = RoomCreationForm(request.POST, request.FILES)

            if form.is_valid():
                room = form.save()
                return student_details_view(request)


        else:
            form = RoomCreationForm()

        context = {'form': form}
        return render(request, 'accounts/add_room.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required()
def room_details(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        studs = UserProfile.objects.all()
        studdata = []
        rm = str(tag)
        # print(studs[1].room.no)
        print(rm)
        for x in studs:
            try:
                y = x.room.no
                if y == rm:
                    l = {'name': x.user.first_name, 'username': x.user.username, 'room': x.room.no, 'course': x.course,
                         'fees': x.fees_paid}
                    print(l)
                    studdata.append(l)
            except:
                print('error')

        context = {'studdata': studdata, 'room': tag}
        print(context)
        return render(request, 'accounts/room_stud.html', context)

    else:
        return render(request, 'accounts/testing.html')


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


@login_required
def fee_student_history(request):
    if request.user.groups.filter(name__in=['warden']).exists():
        cuser = request.user
        print(cuser)
        # allfees = Fees.objects.filter(student__user=cuser)
        allfees = Fees.objects.all()
        details = []
        for x in allfees:
            l = {'name': x.student.user.first_name, 'date': x.date_paid, 'approve': x.is_approved}
            print(l)
            details.append(l)

        context = {'details': details}
        print(allfees)
        return render(request, 'accounts/feehistory.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required
def fee_instructions(request):
    try:
        s = Fees.objects.get(student__user__username=request.user)
        # app = Approval.objects.get(requester__user__username=current_user)
        print(s, 'hello')
        return render(request, 'accounts/room_notallowed.html')
    except:
        # try:
        cuser = UserProfile.objects.get(user__username=request.user)
        room = cuser.room
        type = room.room_type
        if type == 'S':
            amount = 15000
        elif type == 'D':
            amount = 12000
        else:
            amount = 9000

        return render(request, 'accounts/topay.html', {'amount': amount})
    # except:
    #     return render(request, 'accounts/detail_view.html')


@login_required
def fee_register(request, tag):
    cuser = request.user
    newfee = Fees()
    newfee.student = UserProfile.objects.get(user=cuser)
    newfee.amount = tag
    newfee.save()
    transaction.commit()
    return redirect('student')


@login_required
def fee_approval_list(request):
    if request.user.groups.filter(name__in=['warden']).exists():
        studfees = Fees.objects.all()
        feedata = []

        for x in studfees:
            if x.is_approved == False:
                l = {'name': x.student.user.first_name, 'course': x.student.course, 'date': x.date_paid,
                     'username': x.student.user.username, 'lname': x.student.user.last_name, 'amount': x.amount}
                feedata.append(l)

        context = {'feedata': feedata}
        print(context)
        return render(request, 'accounts/fee_approval_warden.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required
def fees_approve_confirm(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists() == True:

        feepay = Fees.objects.get(student__user__username=tag)
        userpro = UserProfile.objects.get(user__username=tag)
        feepay.is_approved = True
        userpro.fees_paid = True
        userpro.save()
        feepay.save()
        transaction.commit()

        subject = 'Your Fee Payment has been approved'
        message = 'Your Fee Payment has been approved and accepted by the warden. Login to see your Fee Status.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [feepay.student.user.email]
        send_mail(subject, message, email_from, recipient_list)

        return redirect('feesall')

    else:
        return render(request, 'accounts/testing.html')


@login_required
def fees_approve_reject(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        if request.method == 'POST':
            form = RejectForm(request.POST)

            if form.is_valid():
                msg = request.POST.get('message')
                feepay = Fees.objects.get(student__user__username=tag)
                userpro = UserProfile.objects.get(user__username=tag)

                subject = 'Your Fee Payment has been rejected'
                message = 'Your Fee Payment has been rejected by the warden. Contact your warden for more details. ' \
                          'You can apply from your Profile again. Reason: '
                message = message + msg
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [userpro.user.email]
                send_mail(subject, message, email_from, recipient_list)

                feepay.delete()
                transaction.commit()

                return redirect('feesall')

        else:
            username = tag
            form = RejectForm()
            return render(request, 'accounts/reject_msg_fees.html', {'username': username, 'form': form})


    else:
        return render(request, 'accounts/testing.html')


@login_required
def all_student(request):
    if request.user.groups.filter(name__in=['warden']).exists():
        # allfees = Fees.objects.filter(student__user=cuser)
        allstud = UserProfile.objects.all()
        details = []
        for x in allstud:
            l = {'name1': x.user.first_name, 'name2': x.user.last_name, 'course': x.course, 'approve': x.fees_paid,
                 'room': x.room}
            print(l)

            details.append(l)

        context = {'details': details}
        return render(request, 'accounts/students.html', context)

    else:
        return render(request, 'accounts/testing.html')


@login_required
def student_profile_admin(request, tag):
    if request.user.groups.filter(name__in=['warden']).exists():
        obj = UserProfile.objects.get(user__username=tag)

        try:
            context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                       'gender': obj.gender, 'room': obj.room.no, 'email': obj.user.email,
                       'course': obj.course, 'fees': obj.fees_paid, 'uname': obj.user.username}
        except:
            context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
                       'gender': obj.gender, 'room': 'Not Assigned', 'email': obj.user.email,
                       'course': obj.course, 'fees': obj.fees_paid, 'uname': obj.user.username}

            # context = {'name': obj.user.first_name, 'location': obj.location, 'age': obj.age,
            #            'gender': obj.gender, 'room': obj.room.no}

        return render(request, 'accounts/profile_admin.html', context)

    else:
        return render(request, 'accounts/testing.html')
