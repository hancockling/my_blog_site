from django import forms


class UserForm(forms.Form):
    last_name = forms.CharField(label='姓氏', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    first_name = forms.CharField(label='名字', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    email = forms.EmailField(label="邮箱", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    birth = forms.DateField(label='生日', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    phone = forms.CharField(label='电话', max_length=20, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    school = forms.CharField(label='学校', max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    company = forms.CharField(label='公司', max_length=100, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    profession = forms.CharField(label='职业', max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    address = forms.CharField(label='地址', max_length=100, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control-sm'}))
    aboutme = forms.CharField(label='介绍', max_length=100, required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control-sm'}))
