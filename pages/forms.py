from django import forms


class SiteCommentForm(forms.Form):
    author_name = forms.CharField(
        label='Adınız',
        min_length=2,
        max_length=80,
        strip=True,
        error_messages={
            'required': 'Lütfen adınızı yazın.',
            'min_length': 'Ad en az 2 karakter olmalı.',
            'max_length': 'Ad en fazla 80 karakter olabilir.',
        },
    )
    body = forms.CharField(
        label='Yorumunuz',
        min_length=8,
        max_length=800,
        strip=True,
        widget=forms.Textarea,
        error_messages={
            'required': 'Lütfen yorumunuzu yazın.',
            'min_length': 'Yorum en az 8 karakter olmalı.',
            'max_length': 'Yorum en fazla 800 karakter olabilir.',
        },
    )
    # Botlara karşı gizli alan; insan doldurmamalı
    website = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
    )

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Geçersiz gönderim.')
        return ''

    def clean_author_name(self):
        name = ' '.join(self.cleaned_data['author_name'].split())
        return name

    def clean_body(self):
        return self.cleaned_data['body'].strip()
