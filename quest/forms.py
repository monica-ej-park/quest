from django.forms import *
from quest.models import Record, Action, Quest
#from django.contrib.auth.models import User
from account.models import User

class RecordForm(ModelForm):
    #user = CharField(disabled=True)
    user = ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    #category = ModelChoiceField(queryset=Action.objects.)
    action = ModelChoiceField(queryset=Action.objects.all(), empty_label='받을 경험치를 고르세요.')
    xp = IntegerField(widget=NumberInput(attrs={'readonly':'readonly'}), initial=0)
    #xp = CharField(initial="0xp", widget=TextInput(attrs={'readonly':'readonly'}), disabled=True)#widget=NumberInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Record
        fields = ("user", "action", "memo", 'repeat', 'xp')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['xp'].widget.attrs['readonly'] = True
        self.fields['user'].widget.attrs['readonly'] = True
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})
            field.label = ''



class QuestForm(ModelForm):
    class Meta:
        model = Quest
        fields = ('accomplishment',)