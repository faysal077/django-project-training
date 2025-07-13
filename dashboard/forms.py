from django import forms
from dashboard.models import Training, Batch, Participant, FinancialClearance, Attachment


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'organizer', 'training_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'organizer': forms.TextInput(attrs={'class': 'form-control'}),
            'training_type': forms.Select(attrs={'class': 'form-select'}),
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'start_date', 'end_date', 'start_time', 'end_time',
            'total_training_hours', 'fiscal_year'  # ✅ no batch_number here
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_start_date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_end_date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'id_start_time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'id_end_time'
            }),
            'total_training_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_total_training_hours',
                'readonly': 'readonly'  # 👈 Optional: make this non-editable
            }),
            'fiscal_year': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_fiscal_year',
                'readonly': 'readonly'  # 👈 Optional: also make this auto-filled only
            }),
        }

'''
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'start_date', 'end_date', 'start_time', 'end_time',
            'total_training_hours', 'fiscal_year'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_start_date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_end_date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_start_time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_end_time'}),
            'total_training_hours': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_total_training_hours'}),
            'fiscal_year': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_fiscal_year'}),
        }
'''
'''
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'start_date', 'end_date', 'start_time', 'end_time',
            'total_training_hours', 'fiscal_year', 'batch_number'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_start_date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_end_date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'id_start_time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'id_end_time'
            }),
            'total_training_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'id_total_training_hours'
            }),
            'fiscal_year': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'id_fiscal_year'
            }),
            
            'batch_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_batch_number'
            }),
            
        }

'''
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 'Official_ID', 'designation', 'office_address',
            'gender', 'contact', 'email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'}),
            'Official_ID': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_Official_ID'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_designation'}),
            'office_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'id': 'id_office_address'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'id': 'id_gender'}, choices=[
                ('Male', 'Male'),
                ('Female', 'Female')
            ]),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_contact'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 'Official_ID', 'designation', 'office_address',
            'gender', 'contact', 'email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'Official_ID': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'office_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Male', 'Male'),
                ('Female', 'Female')
            ]),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class FinancialClearanceForm(forms.ModelForm):
    class Meta:
        model = FinancialClearance
        fields = ['amount_spent', 'advance_receiver', 'adjustment_info']
        widgets = {
            'amount_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_receiver': forms.TextInput(attrs={'class': 'form-control'}),
            'adjustment_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'file_path']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file_path': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
