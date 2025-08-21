from django import forms
from account.models import  InstituteDetail,ProjectPIDetail, ProjectDetail,FinancialDetail

class InstituteDetailForm(forms.ModelForm):
    class Meta:
        model = InstituteDetail
        fields = ['name', 'sortcode', 'institute_type', 'contactno', 'state','district','address']
        widgets = {
                'address': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            }

class ProjectPIDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectPIDetail
        fields = ['name','dob','gender','qualification','designation','area_expertise','institute', 'contactno', 'emailid','address','state_pi','district_pi']
        widgets = {
                'address': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            }


class ProjectDetailForm(forms.ModelForm):
    duration = forms.CharField(
        label="Read-Only Field",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ProjectDetail
        fields = ['projectpi', 'projectid', 'title', 'filenumber','eofficnumber','duration','approvalfile','proposalfile','prcrecommend','prccomment','prccomment','start_date','end_date','prc_date']

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')

            if start_date and end_date and end_date < start_date:
                self.add_error('end_date', "End date must be after the start date.")
            return cleaned_data


class FinancialDetailForm(forms.ModelForm):
    class Meta:
        model = FinancialDetail
        fields = ['projectpi', 'projectdetail', 'year', 'salary', 'contingencies','non_contingencies','recurring','travel','overhead_expens','total']
        

