from django import forms
import re
import os

class PackageDetectionForm(forms.Form):
    video_source = forms.CharField(label='Video Source')
    phone_number = forms.CharField(label='Phone Number')

    def clean_video_source(self):

        video_source = self.cleaned_data['video_source']

        if re.match(r'^(?:http|ftp|rtsp)s?://', video_source):
            return video_source
    
        if os.path.isfile(video_source):
            return video_source

        if int(video_source) in range(0,5):
            video_source = int(video_source)
            return video_source
            
        raise forms.ValidationError("Invalid URL or file path")
        

    def clean_phone_number(self):

        phone_number = self.cleaned_data['phone_number']
        phone_number = re.sub(r'\D', '', phone_number)

        if len(phone_number) != 10:
            raise forms.ValidationError("Invalid phone number")
        return '+1' + phone_number
        