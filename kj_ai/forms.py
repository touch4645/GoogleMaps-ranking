from django import forms
import re
from bs4 import BeautifulSoup
import requests

class InputUrlForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InputUrlForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    url_str = forms.CharField(max_length=60, required=True, label='URL')


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
