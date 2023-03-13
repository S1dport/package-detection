from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import request, HttpResponse

from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.conf import settings

from mainApp.models import Alert

import cv2
import numpy as np
from datetime import datetime
from twilio.rest import Client
from . import keys
from roboflow import Roboflow
from .forms import PackageDetectionForm




# Create your views here.

class User_LoginView(LoginView):
    template_name = 'mainApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Alerts')

class User_Registration(FormView):
    template_name='mainApp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('Alerts')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(User_Registration, self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('Alerts')
        return super(User_Registration, self).get(*args,**kwargs)

class Alert_ListView(LoginRequiredMixin, ListView):
    model = Alert
    ordering = ['-date']
    context_object_name = 'Alerts'
    paginate_by = 5
    

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset =  queryset.filter(user=self.request.user)
        return queryset

class Alert_DeleteView(LoginRequiredMixin, DeleteView):
    model = Alert
    context_object_name = 'Alerts'
    success_url = reverse_lazy('Alerts')

@login_required
def package_detection(request):
    capture = False
    form = PackageDetectionForm(request.POST)


    if request.method == 'POST':


        if form.is_valid():
           

            video_source = form.cleaned_data['video_source']
            phone_number = form.cleaned_data['phone_number']

            action = request.POST.get('action') 

            if action == 'Start':
                capture = True

            elif action == 'Stop':
                capture = False    

            #twilio api keys
            account_sid = keys.twilio_account_sid
            auth_token = keys.twilio_auth_token
            client = Client(account_sid, auth_token)

            #roboflow api keys
            rf = Roboflow(api_key=keys.Roboflow_api_key)
            project = rf.project("packages-v4")
            model = project.version(6).model

            cap = cv2.VideoCapture(video_source)
            fps = round((cap.get(cv2.CAP_PROP_FPS)), 0)
            
            frame_count=0

            while capture:

                ret, frame = cap.read()

                frame_count += 1
                if not np.all(ret):
                    break

                # check every 5 seconds
                if frame_count % (fps) == 0:
                    predictions = model.predict(frame).json()
                    detections = len(predictions['predictions'])

                    try:
                        latest_alert = Alert.objects.filter(user=request.user).latest('date')
                        num_packages = latest_alert.num_packages
                    except Alert.DoesNotExist:
                        num_packages = 0

                
                    if detections > num_packages:
                        now = datetime.now()
                        current_date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

                        # create an Alert object in the database
                        alert = Alert(user=request.user, num_packages=detections, status='Object Detected', complete=False)
                        alert.save()

                        image_path = 'alert_images/' + str(alert.id) + '.jpg'
                        image_data = cv2.imencode('.jpg', frame)[1].tostring()
                        alert.image.save(image_path, ContentFile(image_data))
                        alert.save()
                        
                        # send a message using Twilio
                        message = client.messages.create(
                            body= f"Object detected at {current_date_time}\nNumber of objects detected: {detections}",
                            from_="+19519043642",
                            to=phone_number
                            )

                    elif detections < num_packages:
                        now = datetime.now()
                        current_date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

                        # create an Alert object in the database
                        alert = Alert(user=request.user, num_packages=detections, status='Object Removed', complete=False)
                        alert.save()

                        image_path = 'alert_images/' + str(alert.id) + '.jpg'
                        image_data = cv2.imencode('.jpg', frame)[1].tostring()
                        alert.image.save(image_path, ContentFile(image_data))
                        alert.save()
                        
                        # send a message using Twilio
                        message = client.messages.create(
                            body= f"Object removed at {current_date_time}\nNumber of objects detected: {detections}",
                            from_="+19519043642",
                            to=phone_number
                            )

                # check for user input to stop 
                action = request.POST.get('action')
                if action == 'Stop':
                    capture = False

            cap.release()

    return render(request, 'mainApp/package_detection.html', {'form':form})



