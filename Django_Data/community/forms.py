from django.forms import ModelForm
from community.models import *

class Form(ModelForm):
	class Meta:
		model = Article
		fields = ['user_info','program_info','user_img', 'content_img']
	def __init__(self, *args, **kwargs):
		super(Form, self).__init__(*args, **kwargs)
		self.fields['user_img'].required = False
		self.fields['content_img'].required = False
