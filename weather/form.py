from django import forms

class ContactForm(forms.Form):
    # emailid = forms.EmailField(label='emailid', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter email id'}), required=True)
    # subject = forms.CharField(label='subject', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter subject'}), required=True)
    # message = forms.CharField(label='message', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Message'}), required=True)
    from_email = forms.EmailField(widget=forms.TextInput(attrs={"class": "w-full rounded-md border border-[#e0e0e0] bg-slate-950 py-3 px-6 text-[#6B7280] outline-none focus:border-yellow-400 focus:ring-1 focus:outline-none focus:ring-yellow-600 focus:shadow-md", "placeholder": "Enter your email"}), required=True)
    full_name = forms.EmailField(widget=forms.TextInput(attrs={"class": "w-full rounded-md border border-[#e0e0e0] bg-slate-950 py-3 px-6 text-[#6B7280] outline-none focus:border-yellow-400 focus:ring-1 focus:outline-none focus:ring-yellow-600 focus:shadow-md", "placeholder": "Enter your name"}), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={"class": "w-full rounded-md border border-[#e0e0e0] bg-slate-950 py-3 px-6 text-[#6B7280] outline-none focus:border-yellow-400 focus:ring-1 focus:outline-none focus:ring-yellow-600 focus:shadow-md", "placeholder": "Enter your subject"}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "w-full resize-none rounded-md border border-[#e0e0e0] bg-slate-950 py-3 px-6 text-[#6B7280] outline-none focus:border-yellow-400 focus:ring-1 focus:outline-none focus:ring-yellow-600 focus:shadow-md", "placeholder": "Type your message"}), required=True)