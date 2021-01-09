from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User#get_user_model()
        fields = ('email', 'name')