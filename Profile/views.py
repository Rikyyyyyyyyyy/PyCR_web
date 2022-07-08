from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .form import UserCreateForm,FeatureSelectionForm, edit_profile
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
from django.urls import reverse
import base64
from django.template.loader import render_to_string
import stripe
from django.contrib import messages
from faker import Faker
from django.contrib.sites.shortcuts import get_current_site
from python_scripts.Feature_selection.thread import PyCRThread
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .gentoken import generate_token
from django.conf import settings
import logging
from botocore.exceptions import ClientError
import boto3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase
fake = Faker()



stripe.api_key = settings.STRIPE_SECRET_KEY

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

# Create your views here.
def index(request):
    return render(request, 'homepage/index.html')


def projects(request):
    return render(request, 'homepage/projects.html')


def about(request):
    return render(request, 'about/about.html')

def about_cite(request):
    return render(request, 'about/about_cite.html')

def about_contributor(request):
    return render(request, 'about/about_contributor.html')

def about_project(request):
    return render(request, 'about/about_project.html')

def about_support(request):
    return render(request, 'about/about_support.html')

def about_license(request):
    return render(request, 'about/about_license.html')

def about_privacy(request):
    return render(request, 'about/about_privacy.html')

def about_instruction(request):
    return render(request, 'about/about_instruction.html')

def send_activate_email(user, request):
    msg = MIMEMultipart()
    cur_site = get_current_site(request)
    email_subject = "Activate your email"
    email_body = render_to_string('registration/activate.html',{
        'user':user,
        'domain':cur_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    msg['Subject'] = email_subject
    msg['From'] = "pycr@ualberta.ca"
    msg['To'] = user.email
    msg.attach(MIMEText(email_body))

    smtp_obj = smtplib.SMTP('smtp.gmail.com', port=587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login(user="pycr@ualberta.ca", password='tmic2022Tmic')
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()



def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password1'])
            new_user =  Author.objects.create(
                userid=new_user.id,
                user=new_user,
                username=new_user.username,
                email=new_user.email,
            )


            send_activate_email(new_user,request)
            messages.add_message(request,messages.SUCCESS,
                                 'We sent you an email to verify your account. If you did not receive a confirmation email, please check your spam folder.')
            return redirect('login')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        current_user = Author.objects.get(userid=user.id)

        if user and not current_user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox/spam folder')
            return render(request, 'authentication/login.html', context, status=401)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials, try again')
            return render(request, 'authentication/login.html', context, status=401)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Welcome {user.username}')

        return redirect(reverse('home'))

    return render(request, 'registration/login.html')

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
            if isMotabo == "false":
                sample_url = task.sample_file.name
                class_url = task.class_file.name
                sampleName_url = task.sampleName_file.name
                variableName_url = task.variableName_file.name
                motabo_url = 'none'
            else:
                sample_url = 'none'
                class_url = 'none'
                sampleName_url = 'none'
                variableName_url = 'none'
                motabo_url = task.motaboFile.name
            # out = run([sys.executable, '//Users//wenwenli//Desktop//TMIC//PyCRWEB//python_scripts//Feature_selection//PyCR.py',isExternal, str(splitRatio), rocType, tupaType, isMotabo, motabo_url, sample_url, class_url,sampleName_url, variableName_url, scaleType, str(iterations),str(survivalRate),rankingAlgorithm, str(vipComponent), str(task.pk)], shell=False, stdout=PIPE)
            current_user = request.user
            current_user = Author.objects.get(userid=current_user.id)
            pyThread = PyCRThread(isExternal, splitRatio, rocType, tupaType, isMotabo, motabo_url, sample_url, class_url, sampleName_url, variableName_url, scaleType, iterations, survivalRate, rankingAlgorithm, vipComponent, task.pk,task,sent_email,current_user,settings.BASE_DIR)
            pyThread.start()
            return redirect('feature_task_list')
    else:
        form = FeatureSelectionForm()
    return render(request, 'FeatureSelection/upload_task.html', {'form': form})


def delete_feature_task(request, pk):
    user_id = request.user.id
    delete_task = Feature_selection.objects.filter(id=pk).first()
    delete_file_urls = []
    s3 = boto3.resource('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if delete_task.isMotabo:
        delete_file_urls.append(delete_task.motaboFile)
    else:
        delete_file_urls.append(delete_task.sample_file)
        delete_file_urls.append(delete_task.class_file)
        delete_file_urls.append(delete_task.sampleName_file)
        delete_file_urls.append(delete_task.variableName_file)

    if delete_task.project_output:
        s3.Object(bucket_name, delete_task.project_output.name).delete()
    for url in delete_file_urls:
        if url:
            s3.Object(bucket_name, url.name).delete()
    delete_task.delete()
    tasks = Feature_selection.objects.all()
    user_tasks = []
    for i in tasks:
        if getattr(i, 'user_id') == str(user_id):
            user_tasks.append(i)
    return redirect('feature_task_list')
    # return render(request, 'FeatureSelection/task_list.html', {
    #     'tasks': user_tasks
    # })

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

def activate_user(request,uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print("here is the uid")
        print(uid)
        user = Author.objects.get(id=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'registration/activate-failed.html', {"user": user})


def create_presigned_url(request, pk ):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    task = Feature_selection.objects.filter(id=pk).first()
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_name = task.project_output.url
    expiration = settings.AWS_BUCKET_EXPIRE_TIME

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return render(request,object_name)