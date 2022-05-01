from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .form import UserCreateForm,FeatureSelectionForm, edit_profile
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from subprocess import run, PIPE
import sys
from django.conf import settings
import os
from django.urls import reverse
import base64
import shutil
import stripe
from python_scripts.Feature_selection import PyCR
from python_scripts import sent_email



stripe.api_key = settings.STRIPE_SECRET_KEY

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

# Create your views here.
def index(request):
    return render(request, 'homepage/index.html')


def projects(request):
    return render(request, 'homepage/projects.html')


def about(request):
    return render(request, 'about/about.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password1'])
            Author.objects.create(
                userid=new_user.id,
                user=new_user,
                username=new_user.username,
                email=new_user.email,
            )

            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    current_user = Author.objects.get(userid=user_id)
    email = current_user.email
    username = current_user.username
    profile_pic = current_user.profile_pic.url
    context['user_id'] = user_id
    context['email'] = email
    context['username'] = username
    context['image_url'] = profile_pic
    return render(request, "homepage/profile.html", context)

def edit_profile_view(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    try:
        author = Author.objects.get(pk=user_id)
    except Author.DoesNotExist:
        return HttpResponse("Something whent wrong!")
    if author.pk != request.user.pk:
        return HttpResponse("You are not able to edit someone elses account!")
    context = {}
    if request.POST:
        form = edit_profile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            current_user = Author.objects.get(userid=user_id)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            profile_pic = form.cleaned_data['profile_pic']
            current_user.username = username
            current_user.email = email
            current_user.profile_pic = profile_pic
            current_user.save()
            return redirect("profile", user_id=author.pk)
        else:
            form = edit_profile(request.POST, instance= request.user,
                                initial={
                                   "id": author.pk,
                                   "email": author.email,
                                   "username": author.username,
                                   "profile_pic": author.profile_pic,
                                })
            context['form'] = form
    else:
        form = edit_profile(request.POST, instance=request.user,
                            initial={
                               "id": author.pk,
                               "email": author.email,
                               "username": author.username,
                               "profile_pic": author.profile_pic,
                            })
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "homepage/edit_profile.html", context)

def save_temp_profile_image_from_base64String(image_string, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + '/' + str(user.pk)):
            os.mkdir(settings.TEMP+'/'+str(user.pk))
        url = os.path.join(f"{settings.TEMP}/{user.pk}", TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(image_string)
        with storage.open('', 'wb+')as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            image_string += "=" * ((4 - len(image_string) % 4) % 4)
            return save_temp_profile_image_from_base64String(image_string, user)
    return None


def feature_task_list(request):
    user_id =request.user.id
    feature_tasks = Feature_selection.objects.all()
    user_tasks = []
    for i in feature_tasks:
        if getattr(i, 'user_id') == str(user_id):
            user_tasks.append(i)
    return render(request, 'FeatureSelection/task_list.html', {
        'tasks': user_tasks
    })


def feature_upload_task(request):

    if request.method == 'POST':
        form = FeatureSelectionForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            user_id = request.user.id
            task_name = form.cleaned_data['task_name']
            isExternal = form.cleaned_data['isExternal']
            splitRatio = form.cleaned_data['splitRatio']
            rankingAlgorithm = form.cleaned_data['rankingAlgorithm']
            vipComponent = form.cleaned_data['vipComponent']
            rocType = form.cleaned_data['rocType']
            tupaType = form.cleaned_data['tupaType']
            isMotabo = form.cleaned_data['isMotabo']
            scaleType = form.cleaned_data['scaleType']
            iterations = form.cleaned_data['iterations']
            survivalRate = form.cleaned_data['survivalRate']
            motaboFile = form.cleaned_data['motaboFile']
            sample_file = form.cleaned_data['sample_file']
            class_file = form.cleaned_data['class_file']
            sampleName_file = form.cleaned_data['sampleName_file']
            variableName_file = form.cleaned_data['variableName_file']
            sent_email = form.cleaned_data['sent_email']
            task = Feature_selection.objects.create(user_id=user_id, task_name=task_name, isExternal=isExternal, splitRatio=splitRatio, rankingAlgorithm=rankingAlgorithm,vipComponent=vipComponent, rocType=rocType, tupaType=tupaType, isMotabo = isMotabo, scaleType=scaleType, iterations= iterations, survivalRate=survivalRate, motaboFile=motaboFile,  sample_file=sample_file, class_file=class_file, sampleName_file=sampleName_file, variableName_file=variableName_file, sent_email=sent_email)
            task.save()
            if isMotabo == 'False':
                sample_url = task.sample_file.path
                class_url = task.class_file.path
                sampleName_url = task.sampleName_file.path
                variableName_url = task.sampleName_file.path
                motabo_url = 'none'
            else:
                sample_url = 'none'
                class_url = 'none'
                sampleName_url = 'none'
                variableName_url = 'none'
                motabo_url = task.motaboFile.path
            # out = run([sys.executable, '//Users//wenwenli//Desktop//TMIC//PyCRWEB//python_scripts//Feature_selection//PyCR.py',isExternal, str(splitRatio), rocType, tupaType, isMotabo, motabo_url, sample_url, class_url,sampleName_url, variableName_url, scaleType, str(iterations),str(survivalRate),rankingAlgorithm, str(vipComponent), str(task.pk)], shell=False, stdout=PIPE)
            PyCR.main(isExternal, splitRatio, rocType, tupaType, isMotabo, motabo_url, sample_url, class_url, sampleName_url, variableName_url, scaleType, iterations, survivalRate, rankingAlgorithm, vipComponent, task.pk)
            shutil.make_archive('static/images/featureSelection/temp/zipOutput/output' + str(task.pk), "zip", 'static/images/featureSelection/temp/output/','output' + str(task.pk))
            task.project_output.name = '/featureSelection/temp/zipOutput/output' + str(task.pk) + ".zip"
            task.save()
            current_user = request.user
            current_user = Author.objects.get(userid=current_user.id)
            if sent_email:
                # sent_mail_out = run([sys.executable,
                #            '//Users//wenwenli//Desktop//TMIC//PyCRWEB//python_scripts//sent_email.py',
                #           current_user.email,'/static/images/featureSelection/temp/zipOutput/output'+str(task.pk)+'.zip', settings.BASE_DIR,current_user.username,task.task_name, task.isExternal, task.rankingAlgorithm, task.rocType, task.tupaType, task.scaleType,str(task.iterations),str(task.survivalRate)], shell=False, stdout=PIPE)
                sent_email.send_mail(current_user.email,'/static/images/featureSelection/temp/zipOutput/output'+str(task.pk)+'.zip', settings.BASE_DIR,current_user.username,task.task_name, task.isExternal, task.rankingAlgorithm, task.rocType, task.tupaType, task.scaleType,task.iterations,task.survivalRate)
            return redirect('feature_task_list')
    else:
        form = FeatureSelectionForm()
    return render(request, 'FeatureSelection/upload_task.html', {'form': form})


def delete_feature_task(request, pk):
    user_id = request.user.id
    delete_task = Feature_selection.objects.filter(id=pk).first()
    delete_task.delete()
    tasks = Feature_selection.objects.all()
    user_tasks = []
    for i in tasks:
        if getattr(i, 'user_id') == str(user_id):
            user_tasks.append(i)
    return render(request, 'FeatureSelection/task_list.html', {
        'tasks': user_tasks
    })

def buyMeCoffee(request):
    return render(request, 'Stripe/buyMeCoffee.html')

def stripe_charge(request):
    amount = int(request.POST['amount'])
    current_user = request.user
    current_user = Author.objects.get(userid=current_user.id)

    if request.method == 'POST':
        customer = stripe.Customer.create(
            email=current_user.email,
            name=current_user.username,
            source=request.POST['stripeToken'],
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='cad',
            description="donation",
        )
    return redirect(reverse('success', args=[amount]))


def stripe_success(request,args):
    amount = args
    return render(request, 'Stripe/success.html', {'amount':amount})