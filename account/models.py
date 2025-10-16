from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    dummy = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
class District(models.Model):
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    dummy = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class InstituteDetail(models.Model):
    user                    = models.ForeignKey(User, null=True, blank=True, related_name='user_institute_detail', on_delete=models.CASCADE, )
    name                    = models.CharField(max_length=100,null=True,blank=True)
    sortcode                = models.CharField(max_length=100,null=True,blank=True)
    INSTITUTE_TYPE_CHOICE   = [('Government', 'Government'), ('Private', 'Private')]
    institute_type          = models.CharField(max_length=100, null=True, blank=True, choices=INSTITUTE_TYPE_CHOICE)
    contactno               = models.CharField(max_length=100,null=True,blank=True)
    state                   = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    district                = models.ForeignKey(District, null=True, on_delete=models.CASCADE)
    address                 = models.CharField(max_length=400,null=True,blank=True)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name}-({self.sortcode})'

class ProjectPIDetail(models.Model):
    user            = models.ForeignKey(User, null=True, blank=True, related_name='user_projectpi_detail', on_delete=models.CASCADE, )
    institute       = models.ForeignKey(InstituteDetail, null=True, blank=True, related_name='institute_projectpi_detail', on_delete=models.CASCADE, )
    name            = models.CharField(max_length=100,null=True,blank=True)
    dob             = models.DateField(null=True,blank=True)
    GENDER_TYPE_CHOICE   = [('Male', 'Male'), ('Female', 'Female')]
    gender          = models.CharField(max_length=100, null=True, blank=True, choices=GENDER_TYPE_CHOICE)
    QUALIFICATION_TYPE_CHOICE   = [('MBBS', 'MBBS'), ('MD', 'MD'),('MSC', 'MSC'),('Phd','Phd'),('M.Tech','M.Tech'),('Other','Other')]
    qualification   = models.CharField(max_length=100, null=True, blank=True, choices=QUALIFICATION_TYPE_CHOICE)
    qualification_other   = models.CharField(max_length=100,null=True,blank=True)
    designation     = models.CharField(max_length=100,null=True,blank=True)
    area_expertise  = models.CharField(max_length=100,null=True,blank=True)
    contactno       = models.CharField(max_length=100,null=True,blank=True)
    emailid         = models.EmailField(max_length=100,null=True,blank=True)
    address         = models.CharField(max_length=200,null=True,blank=True)
    state_pi        = models.ForeignKey(State, null=True,blank=True, on_delete=models.CASCADE)
    district_pi     = models.ForeignKey(District, null=True,blank=True, on_delete=models.CASCADE)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-({self.state_pi.name})"

class ProjectDetail(models.Model):
    user                = models.ForeignKey(User, null=True, blank=True, related_name='user_project_detail', on_delete=models.CASCADE, )
    projectpi           = models.ManyToManyField(ProjectPIDetail,related_name='project_projectpi')
    PROJECT_TYPE_CHOICE   = [('adhoc','Adhoc'),('center_adv_research','Center for Advanced Research(CAR)'),('fellowship', 'Fellowship'),('intermediate','Intermediate'),('NHRP','NHRP'),('small_grant', 'Small Grant'), ('taskforce', 'Taskforce')]
    project_type        = models.CharField(max_length=100, null=True, blank=True, choices=PROJECT_TYPE_CHOICE)
    projectid           = models.CharField(max_length=200,null=True,blank=True)
    title               = models.CharField(max_length=200,null=True,blank=True)
    filenumber          = models.CharField(max_length=200,null=True,blank=True)
    eofficnumber        = models.CharField(max_length=200,null=True,blank=True)
    duration            = models.IntegerField(default=0)
    approvalfile        = models.FileField(upload_to='pdfs/',null=True,blank=True)
    proposalfile        = models.FileField(upload_to='pdfs/',null=True,blank=True)
    PRC_STATUS_CHOICE   = [('Approved', 'Approved'), ('Rejected', 'Rejected')]
    prcrecommend        = models.CharField(max_length=100, null=True, blank=True, choices=PRC_STATUS_CHOICE)
    prccomment          = models.CharField(max_length=100,null=True,blank=True)
    start_date          = models.DateField(null=True,blank=True)
    end_date            = models.DateField(null=True,blank=True)
    prc_date            = models.DateField(null=True,blank=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.projectid}'
    
class FinancialDetail(models.Model):
    YEAR_CHOICE         = [('1st', 'First Year'), ('2nd', 'Second Year'), ('3rd', 'Third Year'),('4th', 'Fourth Year'),('5th', 'Five Year')]
    UC_FLAG             = [('YES', 'YES'), ('NO', 'NO'),]
    user                = models.ForeignKey(User, null=True, blank=True, related_name='user_financial_detail', on_delete=models.CASCADE, )
    projectpi           = models.ForeignKey(ProjectPIDetail, null=True, blank=True, related_name='projectpi_financial_detail', on_delete=models.CASCADE, )
    projectdetail       = models.ForeignKey(ProjectDetail, null=True, blank=True, related_name='projectdetail_financial_detail', on_delete=models.CASCADE, )
    year                = models.CharField(max_length=200,null=True,blank=True)
    salary              = models.FloatField(default=0.00)
    contingencies       = models.FloatField(default=0.00)
    non_contingencies   = models.FloatField(default=0.00)
    recurring           = models.FloatField(default=0.00)
    travel              = models.FloatField(default=0.00)
    overhead_expens     = models.FloatField(default=0.00)
    total               = models.FloatField(default=0.00)
    comment             = models.CharField(max_length=200,null=True,blank=True)
    interest            = models.FloatField(default=0.00)
    remainamount        = models.FloatField(default=0.00)
    carry_forward_amount = models.FloatField(default=0.00)
    subtotal             = models.FloatField(default=0.00)
    remain_tr_amount    = models.FloatField(default=0.00)
    interest_tr_amount  = models.FloatField(default=0.00)
    transfer_from_to    = models.CharField(max_length=200,null=True,blank=True)
    uc_submit           = models.CharField(max_length=100,default='NO', choices=UC_FLAG)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)

    def calculate_subtotal(self):
        return (
            float(self.total) +
            float(self.interest) +
            float(self.carry_forward_amount)
        )

    def calculate_total(self):
        return (
            float(self.salary) +
            float(self.contingencies) +
            float(self.non_contingencies) +
            float(self.recurring) +
            float(self.travel) +
            float(self.overhead_expens)
        )

    def save(self, *args, **kwargs):
        self.total = self.calculate_total()
        self.subtotal = self.calculate_subtotal()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.year}-{self.projectpi}-{self.projectdetail}'

    # def update_total_amount(self, pi_id, project_id):
    #     total = ReleaseBuget.objects.filter(
    #         projectpi_id=pi_id,
    #         projectdetail_id=project_id,
    #         financial_id=self
    #     ).aggregate(sum_total=Sum('total'))['sum_total'] or 0
    #     print("total remainamount",total)
    #     print(type(total))
    #     self.remainamount = total
    #     self.save()
    #     return total

class ReleaseBuget(models.Model):
    user                = models.ForeignKey(User, null=True, blank=True, related_name='user_release_detail', on_delete=models.CASCADE, )
    projectpi           = models.ForeignKey(ProjectPIDetail, null=True, blank=True, related_name='projectpi_release_detail', on_delete=models.CASCADE, )
    projectdetail       = models.ForeignKey(ProjectDetail, null=True, blank=True, related_name='projectdetail_release_detail', on_delete=models.CASCADE, )
    finance             = models.ForeignKey(FinancialDetail, null=True, blank=True, related_name='financial_release_detail', on_delete=models.CASCADE, )
    release_no          = models.CharField(max_length=100,null=True,blank=True)
    year                = models.CharField(max_length=200,null=True,blank=True)
    salary              = models.FloatField(default=0.00)
    contingencies       = models.FloatField(default=0.00)
    non_contingencies   = models.FloatField(default=0.00)
    recurring           = models.FloatField(default=0.00)
    travel              = models.FloatField(default=0.00)
    overhead_expens     = models.FloatField(default=0.00)
    total               = models.FloatField(default=0.00)
    comment             = models.CharField(max_length=200,null=True,blank=True)
    fileupload          = models.FileField(upload_to='pdfs/',null=True,blank=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('projectpi', 'projectdetail', 'finance', 'release_no')
    
    def generate_series_number(self):
        # self.finance
        fin_obj = FinancialDetail.objects.filter(id=self.finance_id,projectpi_id=self.projectpi,projectdetail_id=self.projectdetail).first()
        last = ReleaseBuget.objects.filter(
                projectpi_id=self.projectpi,
                projectdetail_id=self.projectdetail,
                finance_id=self.finance
            ).order_by('-release_no').first()
        if last:
            last_split = int(last.release_no.split('-')[2])
            seq = last_split + 1
            get_year = f'{fin_obj.year}-release-{seq}'
            # last.release_no + 1
            print('last',last)
            return get_year
            # f'{last.finance.year}-release-{1}'
        return f'{fin_obj.year}-release-{1}'

    def save(self, *args, **kwargs):
        
        if self._state.adding:  # Only generate for new records
            if self.release_no is None:
                self.release_no = self.generate_series_number()
                # self.release_no.save()
        
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.id)

class UsedBalance(models.Model):
    user                = models.ForeignKey(User, null=True, blank=True, related_name='user_ub_detail', on_delete=models.CASCADE, )
    projectpi           = models.ForeignKey(ProjectPIDetail, null=True, blank=True, related_name='projectpi_ub_detail', on_delete=models.CASCADE, )
    projectdetail       = models.ForeignKey(ProjectDetail, null=True, blank=True, related_name='projectdetail_ub_detail', on_delete=models.CASCADE, )
    finance             = models.ForeignKey(FinancialDetail, null=True, blank=True, related_name='financial_ub_detail', on_delete=models.CASCADE, )
    uc_no               = models.CharField(max_length=200,null=True,blank=True)
    year                = models.CharField(max_length=200,null=True,blank=True)
    salary              = models.FloatField(default=0.00)
    contingencies       = models.FloatField(default=0.00)
    non_contingencies   = models.FloatField(default=0.00)
    recurring           = models.FloatField(default=0.00)
    travel              = models.FloatField(default=0.00)
    overhead_expens     = models.FloatField(default=0.00)
    total               = models.FloatField(default=0.00)
    comment             = models.CharField(max_length=200,null=True,blank=True)
    fileupload          = models.FileField(upload_to='pdfs/',null=True,blank=True)
    interest            = models.FloatField(default=0.00)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)


    def carry_forward_to_next_year(self):
        finance_year = ['1st','2nd','3rd','4th','5th']
        # FinancialDetail.objects.filter(id=self.finance.id,projectpi_id=self.projectpi,projectdetail_id=self.projectdetail).first()
        print('self',self)
        
        year_obj = FinancialDetail.objects.filter(id=self.finance.id).first()
        current_year = year_obj.year
        current_interest = self.interest
        current_remain_amount = year_obj.remainamount
        print('current_year',current_year)
        getyear_index = finance_year.index(current_year)
        nextyear_index = getyear_index + 1 
        try:
            next_year = finance_year[nextyear_index]
        except IndexError as e:
            next_year = None
        if next_year:    
            nextyear_obj = FinancialDetail.objects.filter(year=next_year,projectpi_id=self.projectpi,projectdetail_id=self.projectdetail).first()
            if nextyear_obj:
                nextyear_obj.carry_forward_amount = float(current_interest) + float(current_remain_amount)
                nextsubtotal = nextyear_obj.save()
                # nextsubtotal.calculate_subtotal()
                year_obj.interest = current_interest
                year_obj.remain_tr_amount = current_remain_amount
                year_obj.interest_tr_amount = current_interest
                year_obj.transfer_from_to = f'{current_year}->{next_year}'        
                year_obj.uc_submit='YES'
                year_obj.save()
        # else:
        year_obj.interest = current_interest        
        year_obj.uc_submit='YES'
        year_obj.save()


    def generate_series_number_uc(self):
        # self.finance
        fin_obj = FinancialDetail.objects.filter(id=self.finance.id,projectpi_id=self.projectpi,projectdetail_id=self.projectdetail).first()
        last = UsedBalance.objects.filter(
                projectpi_id=self.projectpi,
                projectdetail_id=self.projectdetail,
                finance_id=self.finance
            ).order_by('-uc_no').first()
        if last:
            last_split = int(last.uc_no.split('-')[2])
            seq = last_split + 1
            get_year = f'{fin_obj.year}-uc-{seq}'
            # last.release_no + 1
            print('last',last)
            return get_year
            # f'{last.finance.year}-release-{1}'
        return f'{fin_obj.year}-uc-{1}'

    def save(self, *args, **kwargs):
        total_released = ReleaseBuget.objects.filter(projectpi_id=self.projectpi,projectdetail_id=self.projectdetail,finance_id=self.finance).aggregate(
                total=models.Sum('total')
            )['total'] or 0    
        print('total_released',total_released)
        remaining = total_released - float(self.total)
        print('remaining',remaining)

        self.finance.remainamount = remaining
        self.finance.save(update_fields=['remainamount'])
        self.carry_forward_to_next_year()
        if self._state.adding:  # Only generate for new records
            if self.uc_no is None:
                self.uc_no = self.generate_series_number_uc()
        super().save(*args, **kwargs)        

    def __str__(self):
        return str(self.id)
