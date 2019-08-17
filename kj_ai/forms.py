from django import forms
import re
from bs4 import BeautifulSoup
import requests

class InputUrlForm(forms.Form):
    url_str = forms.CharField(max_length=255, required=True, label='URL')

    def clean_url_str(self):
        input_url = self.cleaned_data['url_str']
        pattern = 'https:\/\/www\.ufret\.jp\/song\.php\?data=[0-9]+'
        if re.search(pattern, input_url) is None:
            raise forms.ValidationError('URLが正しくありません')

        url = re.search(pattern, input_url).group()
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if soup.find('title').text.split('/')[0] == ' ':
            raise forms.ValidationError('URLが正しくありません')

        return url