from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import  ProjectPIDetail, ProjectDetail,FinancialDetail,InstituteDetail,District,State,ReleaseBuget,UsedBalance,BalanceSheet
from account.forms import ProjectPIDetailForm, ProjectDetailForm, FinancialDetailForm,InstituteDetailForm
import os
import json
import datetime
from datetime import datetime
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime, timedelta, timezone
from django.db.models import Count

# Create your views here.
@login_required(login_url="login")
def home(request):
    pi_name = request.GET.get('Dr ABC', '')
    project_type = request.GET.get('adhoc', '')
    pi_name = ''
    project_type = ''
    prcreccomend_type = ''
    state = ''
    district = ''
    start = datetime(2025, 8, 20, tzinfo=timezone.utc)
    end = datetime(2025, 11, 1, tzinfo=timezone.utc)

    project_count = []
    project_type_count = []
    project_type_count_dict = {}
    project_pi_count = {}
    pi_project_count = {}
    pi_project_list = []
    context = {}
    filters = Q()
    if pi_name:
        filters &= Q(projectpi__name=pi_name)
    if project_type:
        filters &= Q(projectdetail__project_type=project_type)
    if prcreccomend_type:
        filters &= Q(projectdetail__prcrecommend=prcreccomend_type)
    if state:
        state_id = State.objects.filter(name=state).first()
        filters &= Q(projectpi__state_pi_id=state_id)
    if district:
        district_id = District.objects.filter(name=district).first()
        filters &= Q(projectpi__district_pi_id=district_id)
    if start and end:
        filters &= Q(projectdetail__created__gte=start, projectdetail__created__lt=end)

    finance = FinancialDetail.objects.select_related('projectpi','projectdetail').filter(filters)
    
    
    for detail in finance:
        if detail.projectdetail.id not in project_type_count:
            project_type_count.append(detail.projectdetail.id)
            project_count.append(detail.projectdetail.id)
            print('project type',detail.projectdetail.project_type)
            if detail.projectdetail.project_type not in project_type_count_dict:
                project_type_count_dict[detail.projectdetail.project_type] = 1
            else:
                project_type_count_dict[detail.projectdetail.project_type] += 1
            print(detail.projectpi.name)
            print(detail.projectdetail.title)
            
            if detail.projectpi.name in project_pi_count:
                project_pi_count[detail.projectpi.name] += 1
                pi_project_count[detail.projectpi.name].append(detail.projectdetail.title)
            else:
                project_pi_count[detail.projectpi.name] = 1
                pi_project_count[detail.projectpi.name]=[detail.projectdetail.title]
                
    print("project_count",len(project_count))
    print('project_type_count',len(project_type_count))
    print('project_type_count_dict',project_type_count_dict)
    print('project_pi_count',project_pi_count)
    print('pi_project_count',pi_project_count)

    institute_name_obj = InstituteDetail.objects.values('id','name')
    print('institute_name_obj',institute_name_obj)
    context['institute_name_obj']=institute_name_obj

    pi_name_obj = ProjectPIDetail.objects.values('id','name')
    print('pi name',pi_name)
    context['pi_name_obj']=pi_name_obj

    state_name_obj = State.objects.values('id','name')
    print('state_name_obj',state_name_obj)
    context['state_name_obj']=state_name_obj

    district_name_obj = District.objects.values('id','name')
    print('district_name_obj',district_name_obj)
    context['district_name_obj']=district_name_obj
    
    return render(request,'account/home.html',context)

def dashboard_data(request):
    pi_name = request.GET.get('pi_name', '')
    project_type = request.GET.get('project_type', '')
    prc_recommed = request.GET.get('prc_recommed', '')
    institute = request.GET.get('institute', '')
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    print('pi_name',pi_name)
    print('project_type',project_type)
    print('prc_recommed',prc_recommed)
    print('institute',institute)
    print('state',state)
    print('district',district)
    print('start_date',start_date)
    print('end_date',end_date)

    pi_name = ''
    project_type = ''
    prcreccomend_type = ''
    state = ''
    district = ''
    start = datetime(2025, 8, 20, tzinfo=timezone.utc)
    end = datetime(2025, 11, 1, tzinfo=timezone.utc)

    project_count = []
    project_type_count = []
    project_type_count_dict = {}
    project_pi_count = {}
    pi_project_count = {}
    pi_project_list = []
    context = {}
    filters = Q()
    if pi_name:
        filters &= Q(projectpi__name=pi_name)
    if project_type:
        filters &= Q(projectdetail__project_type=project_type)
    if prcreccomend_type:
        filters &= Q(projectdetail__prcrecommend=prcreccomend_type)
    if state:
        state_id = State.objects.filter(name=state).first()
        filters &= Q(projectpi__state_pi_id=state_id)
    if district:
        district_id = District.objects.filter(name=district).first()
        filters &= Q(projectpi__district_pi_id=district_id)
    if start and end:
        filters &= Q(projectdetail__created__gte=start, projectdetail__created__lt=end)

    finance = FinancialDetail.objects.select_related('projectpi','projectdetail').filter(filters)
    
    
    for detail in finance:
        if detail.projectdetail.id not in project_type_count:
            project_type_count.append(detail.projectdetail.id)
            # project_count.append(detail.projectdetail.id)
            # print('project type',detail.projectdetail.project_type)
            if detail.projectdetail.project_type not in project_type_count_dict:
                project_type_count_dict[detail.projectdetail.project_type] = 1
            else:
                project_type_count_dict[detail.projectdetail.project_type] += 1
            # print(detail.projectpi.name)
            # print(detail.projectdetail.title)
            
            if detail.projectpi.name in project_pi_count:
                project_pi_count[detail.projectpi.name] += 1
                pi_project_count[detail.projectpi.name].append(detail.projectdetail.title)
            else:
                project_pi_count[detail.projectpi.name] = 1
                pi_project_count[detail.projectpi.name]=[detail.projectdetail.title]
                
    # print("project_count",len(project_count))
    # print('project_type_count',len(project_type_count))
    # print('project_type_count_dict',project_type_count_dict)
    # print('project_pi_count',project_pi_count)
    # print('pi_project_count',pi_project_count)

    return JsonResponse({'message':"Successfully fetch data..."})
    
def loginpage(request):
    return render(request,'account/login.html')

def loginview(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print('user',user)
        if user is not None:
            login(request,user)
            return JsonResponse({"message":"Login Successfully","status":"200 OK"})
        else:
            return JsonResponse({'message':"No username and password!"}, status=401)    
    return JsonResponse({'message':"No username and password!"})

def logoutview(request):
    logout(request)
    return redirect('login')
    
@login_required(login_url="login")
def projectentry(request):
    institute_form = InstituteDetailForm()
    pi_form = ProjectPIDetailForm()
    pro_form = ProjectDetailForm()
    fin_form = FinancialDetailForm()
    context = {'institute_form':institute_form,'pi_form':pi_form,'pro_form':pro_form,'fin_form':fin_form}
    return render(request,'account/projectentry.html',context)
@login_required(login_url="login")
def load_districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).order_by('name')
    data = [{'id': district.id, 'name': district.name} for district in districts]
    return JsonResponse(data, safe=False)

@login_required(login_url="login")
def pidetailsave(request):
    form = ProjectPIDetailForm(request.POST)
    name_title = request.POST.get('name_title')
    name = request.POST.get('name')
        
    if form.is_valid():
        form_save = form.save(commit=False)
        form_save.user = request.user
        form_save.name = f'{name_title} {name}'
        form_save.save() 
        return JsonResponse({'id': form_save.id, 'name': form_save.name,'message':'Form submit successfully!!','status':'200 OK'})
    else:
        # print(form.errors)
        return JsonResponse({'message':"Please check it. Something went wrong.",'status':'403'})     


@login_required(login_url="login")
def proejct_detailsave(request):
    form = ProjectDetailForm(request.POST, request.FILES)
    print(request.POST)
    pi_ids = request.POST.getlist('projectpi')
    projectid = request.POST.get('projectid')
    filenumber = request.POST.get('filenumber')
    # print('filenumber',filenumber)
    pdffile = request.FILES['proposalfile']
    filename =  pdffile.name
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    # print(type(start_date))
    # print(end_date)
    startdate = datetime.strptime(start_date, "%Y-%m-%d")
    enddate = datetime.strptime(end_date, "%Y-%m-%d")
    # print('startdate',type(startdate))
    # print('startdate',startdate)
    try:
        project_obj = ProjectDetail.objects.filter(projectid=projectid).first()
        projectid_exist = project_obj.projectid
    except AttributeError:
        projectid_exist = ""

    # pdb.set_trace()

    try:
        filenumber_obj = ProjectDetail.objects.filter(filenumber=filenumber).first()
        filenumber_exist = filenumber_obj.filenumber
    except AttributeError:
        filenumber_exist = ""

    filenamelength = len(filename)
    extension = os.path.splitext(filename)[1]
    split_filename = filename.split('.')

    check_list = []
    for i in split_filename[0]:
        if i in {'*','+','?','$','^','(',')','[',']','|','`\`,%'}:
            check_list.append(i)
    
    if len(filename) > 20:
        return JsonResponse({'message':'File Name should be less than twenty charater only.','status':'403'})
    elif len(split_filename)>2:
        return JsonResponse({'message':'Multiple dot(.) not allowed in filename','status':'403'})
    elif split_filename[-1] not in {'pdf'}:
        return JsonResponse({'message':'Only allowed pdf extension file','status':'403'})
    elif len(check_list)>1:
        return JsonResponse({'message':'Special and meta charater not allowed.','status':'403'})
    elif startdate >= enddate:
        return JsonResponse({'message':'Start date must be greater than end date','status':'403'})
    elif projectid_exist:
        return JsonResponse({'message':'Check again.., Project id already exists.','status':'403'})
    elif filenumber_exist:
        return JsonResponse({'message':'Check again.., File Number already exists.','status':'403'})    
    else:
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            if pi_ids:
                form_save.projectpi.set(pi_ids)
             
            return JsonResponse({'id': form_save.projectid, 'name': form_save.projectid,'message':'Form submit successfully!!','status':'200 OK'})
        else:
            return JsonResponse({'message':"Please check it. Something went wrong.",'status':'403'})  

@login_required(login_url="login")
def institute_detailsave(request):
    # print(request.POST)
    if request.method == 'POST':
        form = InstituteDetailForm(request.POST)
        sortcode = request.POST.get('sortcode')
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.sortcode = sortcode.upper()
            form_save.save() 
            return JsonResponse({'id': form_save.id, 'name': form_save.name,'message':'Form submit successfully!!','status':'200 OK'})
        else:
            return JsonResponse({'message':"Please check it. Something went wrong.",'status':'403'})
    
@login_required(login_url="login")
def filter_project(request):
    project_id = request.GET.get('projectpi_id')
    project = ProjectDetail.objects.filter(projectpi__id=project_id,prcrecommend='Approved').order_by('title')
    return JsonResponse(list(project.values('id', 'title')), safe=False)
    

@login_required(login_url="login")
def filter_pi_project(request):
    if request.method == 'GET':
        projectid = request.GET.get('projectid')
        fetch_pi = ProjectPIDetail.objects.filter(project_projectpi__projectid=projectid)
        fetch_pidetail = fetch_pi.values('id','name')
        return JsonResponse(list(fetch_pi.values('id','name')), safe=False)

@login_required(login_url="login")
def get_states(request):
    institute_id = request.GET.get('institute_id')
    institute_obj = InstituteDetail.objects.filter(id=institute_id).first()
    states = State.objects.filter(id=institute_obj.state_id).values('id', 'name')
    return JsonResponse(list(states), safe=False)

@login_required(login_url="login")
def get_districts(request):
    institute_id = request.GET.get('institute_id')
    institute_obj = InstituteDetail.objects.filter(id=institute_id).first()

    districts = District.objects.filter(id=institute_obj.district_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

@login_required(login_url="login")
def states(request):
    states = State.objects.filter().values('id', 'name')
    return JsonResponse(list(states), safe=False)

@login_required(login_url="login")
def districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

@login_required(login_url="login")
def filter_projectdetail(request):
    project = ProjectDetail.objects.values('id','title','projectid')
    return JsonResponse(list(project), safe=False)



def fetch_financial_record(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    pi_obj= ProjectDetail.objects.filter(projectid=project_id)
    id_projectdetail = pi_obj[0].id
    qs = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail).values().order_by('year')
    print('projectpi_id',projectpi_id)
    print('project_id',project_id)
    print('id_projectdetail',id_projectdetail)
    
    qs_query = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail).order_by('id')
    # print('qs_query',qs_query[0].id)
    # pdb.set_trace()
    qs_list = []
    
    qs_uc_list = []
    for i in qs_query:
        # print(i.id)
        dict_finance = {}
        dict_finance['id']=i.id
        dict_finance['year']=i.year
        dict_finance['salary']=i.salary
        dict_finance['contingencies']=i.contingencies
        dict_finance['non_contingencies']=i.non_contingencies
        dict_finance['recurring']=i.recurring
        dict_finance['travel']=i.travel
        dict_finance['overhead_expens']=i.overhead_expens
        dict_finance['file']='pdf'
        dict_finance['total']=i.total
        dict_finance['comment']=i.comment
        dict_finance['subtotal']=i.subtotal
        # print(dict_finance)
        qs_release = ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail,finance_id=i.id)
        qs_uc = UsedBalance.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail,finance_id=i.id)
        qs_release_list = []
        if qs_release:
            for d in qs_release:
                dict_release = {}
                dict_release['id']=d.id
                dict_release['year']=d.year
                dict_release['release_no']=d.release_no
                dict_release['salary']=d.salary
                dict_release['contingencies']=d.contingencies
                dict_release['non_contingencies']=d.non_contingencies
                dict_release['recurring']=d.recurring
                dict_release['travel']=d.travel
                dict_release['overhead_expens']=d.overhead_expens
                dict_release['file']='pdf'
                dict_release['total']=d.total
                dict_release['comment']=d.comment
                dict_release['flag']='rel'
                # print('dict_release',dict_release)
                qs_release_list.append(dict_release)
        if qs_uc:
            for u in qs_uc:
                dict_uc = {}
                dict_uc['id']=u.id
                dict_uc['year']=u.year
                dict_uc['uc_no']=u.uc_no
                dict_uc['salary']=u.salary
                dict_uc['contingencies']=u.contingencies
                dict_uc['non_contingencies']=u.non_contingencies
                dict_uc['recurring']=u.recurring
                dict_uc['travel']=u.travel
                dict_uc['overhead_expens']=u.overhead_expens
                dict_uc['file']='pdf'
                dict_uc['total']=u.total
                dict_uc['interest']=u.interest
                dict_uc['comment']=u.comment
                dict_uc['flag']='uc'
                # print('dict_release',dict_uc)
                qs_release_list.append(dict_uc)
        dict_finance['release']=qs_release_list
        qs_list.append(dict_finance)

    print("***********************************************************************")
    print('qs_list',qs_list)            
    return JsonResponse({'data':list(qs),'newData':qs_list}, safe=False)
    
import pdb
@login_required(login_url="login")
def financial_save(request):
    if request.method == 'POST':
        # files = request.FILES.getlist('files') 
        print('data',request.POST)
        # pdb.set_trace()
        # json_data = json.loads(request.POST.get('json_data', '{}'))
        return_data = json.loads(request.POST.get('return_data', '{}'))
        # print('json_data',json_data)
        print("*********************************************************************")
        print('return_data',return_data)
        print("*********************************************************************")
        
        for row in return_data:
            
            idexist = row['id']
            file_key = row['file_key']
            print('file_key',file_key)
            uploaded_file = request.FILES.get(file_key,None)
            if idexist != '000':
                try:
                    obj = FinancialDetail.objects.get(id=idexist)
                    obj.projectpi_id = row['projectpi_id']
                    obj.projectdetail_id = row['projects_id']
                    obj.year = row['inputs']['year_row']
                    obj.salary = row['inputs']['salary_row']
                    obj.contingencies = row['inputs']['contingencies_row']
                    obj.non_contingencies = row['inputs']['noncontingencies_row']
                    obj.recurring = row['inputs']['recurring_row']
                    obj.travel = row['inputs']['travel_row']
                    obj.overhead_expens = row['inputs']['overhead_row']
                    obj.total = row['inputs']['amt']
                    if uploaded_file:
                        obj.fileupload = uploaded_file
                    obj.save()    
                except FinancialDetail.DoesNotExist:
                    return JsonResponse({'message': 'Object id not found','status':'400'})    
                print(" Record already exists going for update mode")
            else:
                FinancialDetail.objects.create(user=request.user,
                projectpi_id = row['projectpi_id'],
                projectdetail_id = row['projects_id'],
                year = row['inputs']['year_row'],
                salary = row['inputs']['salary_row'],
                contingencies = row['inputs']['contingencies_row'],
                non_contingencies = row['inputs']['noncontingencies_row'],
                recurring = row['inputs']['recurring_row'],
                travel = row['inputs']['travel_row'],
                overhead_expens = row['inputs']['overhead_row'],
                total = row['inputs']['amt'],
                fileupload = uploaded_file,
                )
                print('Record is not exist going to create mode')
               
    return JsonResponse({'message':'Form submit successfully!!','status':'200 OK'})


@login_required(login_url="login")
def financial_save_record(request):
    if request.method == 'POST':
        # files = request.FILES.get('uploadfile') 
        print('data',request.POST)
        # print('files',files)
        getid = request.POST.get('id','')
        projectpi_id = request.POST.get('projectpi','')
        projects_id = request.POST.get('projects','')
        year = request.POST.get('year','')
        salary = request.POST.get('salary','')
        contingencies = request.POST.get('contingencies','')
        noncontingencies = request.POST.get('noncontingencies','')
        recurring = request.POST.get('recurring','')
        travel = request.POST.get('travel','')
        overheadexpens = request.POST.get('overheadexpens','')
        total = request.POST.get('total','')
        comment = request.POST.get('comment','')
        print('getid',getid)
        print('projectpi',projectpi_id)
        print('projects',projects_id)
        # project_id = request.GET.get('projects_id')
        pi_obj= ProjectDetail.objects.filter(projectid=projects_id)
        id_projectdetail = pi_obj[0].id
        # pdb.set_trace()
        if getid == 'new':
            # for new finance year create
            obj = FinancialDetail.objects.create(user=request.user,
                projectpi_id = projectpi_id,
                projectdetail_id =id_projectdetail,
                year = year,
                salary = salary,
                contingencies = contingencies,
                non_contingencies = noncontingencies,
                recurring = recurring,
                travel = travel,
                overhead_expens = overheadexpens,
                comment = comment,
                )
            obj.calculate_total()    
            print('Financial details create records')
            return JsonResponse({'message':'Create finance year successfully!!','status':'200 OK'})
        else:
            print('Financial details updated records')        
            return JsonResponse({'message':'Record updated successfully!!','status':'200 OK'})
    return JsonResponse({'message':'Something went wrong!!','status':'400 BAD_REQUEST'})

@login_required(login_url="login")
def release_save_record(request):
    if request.method == 'POST':
        files = request.FILES.get('uploadfile') 
        print('data',request.POST)
        print('files',files)
        getid = request.POST.get('createExistid','')
        finance_id = request.POST.get('senssion_id','')
        projectpi_id = request.POST.get('projectpi','')
        projects_id = request.POST.get('projects','')
        year = request.POST.get('year','')
        salary = request.POST.get('salary','')
        contingencies = request.POST.get('contingencies','')
        noncontingencies = request.POST.get('noncontingencies','')
        recurring = request.POST.get('recurring','')
        travel = request.POST.get('travel','')
        overheadexpens = request.POST.get('overheadexpens','')
        total = request.POST.get('total','')
        comment = request.POST.get('comment','')
        print('getid',getid)
        print('projectpi',projectpi_id)
        print('projects',projects_id)
        pi_obj= ProjectDetail.objects.filter(projectid=projects_id)
        id_projectdetail = pi_obj[0].id
        if year == '':
            return JsonResponse({'message':'Please fill release year','status':'400 BAD_REQUEST'})
        # if year != '':
        #     try:
        #         year_split = year.split('-')[1]
        #         if year_split != 'release':
        #             return JsonResponse({'message':'Please select currect button','status':'400 BAD_REQUEST'})
        #     except IndexError as e:
        #         return JsonResponse({'message':'Please fill currect year of release, Ex. 1st-release-1','status':'400 BAD_REQUEST'})
            
        # pdb.set_trace()
        if getid == 'new':
            ReleaseBuget.objects.create(user=request.user,
                projectpi_id = projectpi_id,
                projectdetail_id =id_projectdetail,
                finance_id = finance_id,  
                year = year,
                salary = salary,
                contingencies = contingencies,
                non_contingencies = noncontingencies,
                recurring = recurring,
                travel = travel,
                overhead_expens = overheadexpens,
                total = total,
                fileupload = files,
                comment = comment,
                )
            print("create new record")
            return JsonResponse({'message':'Create Release successfully!!','status':'200 OK'})
        else:
            release_obj = ReleaseBuget.objects.filter(id=getid).first()
            # release_obj.projectpi_id = projectpi_id
            # release_obj.projectdetail_id =id_projectdetail
            # release_obj.finance_id = finance_id
            release_obj.year = year
            release_obj.salary = salary
            release_obj.contingencies = contingencies
            release_obj.non_contingencies = noncontingencies
            release_obj.recurring = recurring
            release_obj.travel = travel
            release_obj.overhead_expens = overheadexpens
            release_obj.total = total
            if files:
                release_obj.fileupload = files
            release_obj.comment = comment
            release_obj.save()
            print("update record")
            return JsonResponse({'message':'Record updated successfully!!','status':'200 OK'})
    return JsonResponse({'message':'Something went wrong!!','status':'400 BAD_REQUEST'})   


@login_required(login_url="login")
def uc_save_record(request):
    if request.method == 'POST':
        files = request.FILES.get('uploadfile') 
        print('data',request.POST)
        print('files',files)
        getid = request.POST.get('createExistid','')
        projectpi_id = request.POST.get('projectpi','')
        projects_id = request.POST.get('projects','')
        finance_id = request.POST.get('senssion_id','')
        year = request.POST.get('year','')
        salary = request.POST.get('salary','')
        contingencies = request.POST.get('contingencies','')
        noncontingencies = request.POST.get('noncontingencies','')
        recurring = request.POST.get('recurring','')
        travel = request.POST.get('travel','')
        overheadexpens = request.POST.get('overheadexpens','')
        total = request.POST.get('total','')
        comment = request.POST.get('comment','')
        interest = request.POST.get('interest','')
        print('getid',getid)
        print('projectpi',projectpi_id)
        print('projects',projects_id)
        print('finance_id',finance_id)
        pi_obj= ProjectDetail.objects.filter(projectid=projects_id)
        id_projectdetail = pi_obj[0].id
        # pdb.set_trace()
        if year == '':
            return JsonResponse({'message':'Please fill uc year','status':'400 BAD_REQUEST'})
        # if year != '':
        #     year_split = year.split('-')[1]
        #     print('year_split',year_split)
        #     if year_split != 'uc':
        #         return JsonResponse({'message':'Please select currect button','status':'400 BAD_REQUEST'})
        if getid == 'new':
            UsedBalance.objects.create(user=request.user,
                projectpi_id = projectpi_id,
                projectdetail_id =id_projectdetail,
                finance_id = finance_id,  
                year = year,
                salary = salary,
                contingencies = contingencies,
                non_contingencies = noncontingencies,
                recurring = recurring,
                travel = travel,
                overhead_expens = overheadexpens,
                total = total,
                fileupload = files,
                comment = comment,
                interest= interest,
                )
            print("create new record")
            return JsonResponse({'message':'UC create successfully!!','status':'200 OK'})
        else:
            uc_obj = UsedBalance.objects.filter(id = getid).first()
            uc_obj.year = year
            uc_obj.salary = salary
            uc_obj.contingencies = contingencies
            uc_obj.non_contingencies = noncontingencies
            uc_obj.recurring = recurring
            uc_obj.travel = travel
            uc_obj.overhead_expens = overheadexpens
            uc_obj.total = total
            uc_obj.comment = comment
            if files:
                uc_obj.fileupload = files
            uc_obj.save()
            print("update record")
            return JsonResponse({'message':'Record updated successfully!!','status':'200 OK'})
    return JsonResponse({'message':'Something went wrong!!','status':'400 BAD_REQUEST'})   

@login_required(login_url="login")
def autocomplete_area_experties(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term', '')
        suggestions = ProjectPIDetail.objects.filter(area_expertise__icontains=term).values_list('area_expertise', flat=True)[:10]
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([])

@login_required(login_url="login")
def autocomplete_designation(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term', '')
        suggestions = ProjectPIDetail.objects.filter(designation__icontains=term).values_list('designation', flat=True)[:10]
        print('suggestions',suggestions)
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([])

@login_required(login_url="login")
def projectview(request):
    project_list = []
    projects = ProjectDetail.objects.prefetch_related('projectpi__state_pi','projectpi__institute').all()
    for project in projects:
        project_dict = {}
        # print(f"Project: {project.title},ProjectId:{project.projectid}")
        project_dict['projectid']=project.id
        project_dict['project_eofficnumber']=project.eofficnumber
        project_dict['project_filenumber']=project.filenumber
        project_dict['project_title']=project.title
        project_dict['project_id']=project.projectid
        project_dict['project_type']=project.project_type
        for pi in project.projectpi.all():
            # print(f"  PI: {pi.name}, Email: {pi.emailid}, State: {pi.state_pi.name},Institute: {pi.institute.name}")
            project_dict['piid']=pi.id
            project_dict['pi_name']=pi.name
            project_dict['pi_state']=pi.state_pi.name
            project_dict['pi_institute']=pi.institute.name
            project_list.append(project_dict)
            # print(project_dict)
        # print()
    # print(project_list)
    context = {'projects': project_list}
    return render(request,"account/projectview.html",context)

@login_required(login_url="login")
def project_detail_view(request,pk):
    project = get_object_or_404(ProjectDetail,pk=pk)
    form = ProjectDetailForm(request.POST or None,request.FILES or None, instance=project)
    pi_ids = request.POST.getlist('projectpi')
    # print('pi_ids',pi_ids)
    if form.is_valid():
        form_save = form.save(commit=False)
        form_save.user = request.user
        form_save.save()
        print("form updated")
        if pi_ids:
            form_save.projectpi.set(pi_ids)
            return JsonResponse({'message':'Form updated successfully!!','status':'200 OK'})
        else:
            return JsonResponse({'message':"Please check it. Something went wrong.",'status':'403'})  
    context = {'form':form,'projec_detail_id':project.id}
    return render(request,"account/project_detail_view.html",context)

@login_required(login_url="login")
def pi_detail_view(request,pk):
    project = get_object_or_404(ProjectPIDetail,pk=pk)
    form = ProjectPIDetailForm(request.POST or None, instance=project)
    
    if form.is_valid():
        form_save = form.save(commit=False)
        form_save.user = request.user
        form_save.save() 
        print('Form update successfully!!')
        return JsonResponse({'message':'Form update successfully!!','status':'200 OK'})
        # else:
        #     return JsonResponse({'message':"Please check it. Something went wrong.",'status':'403'})  
    print(form.errors)
    context = {'form':form,'pi_id':project.id}
    return render(request,"account/pi_detail_view.html",context)

def fund_details(request):
    projectpi_id = request.GET.get('pi_id')
    id_projectdetail = request.GET.get('project_id')
    print('pi_id fund_details',projectpi_id)
    print('project_id fund_details',id_projectdetail)
    
    qs_query = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail).order_by('id')
    qs_list = []
    
    qs_uc_list = []
    for i in qs_query:
        # print(i.id)
        dict_finance = {}
        dict_finance['id']=i.id
        dict_finance['year']=i.year
        dict_finance['salary']=i.salary
        dict_finance['contingencies']=i.contingencies
        dict_finance['non_contingencies']=i.non_contingencies
        dict_finance['recurring']=i.recurring
        dict_finance['travel']=i.travel
        dict_finance['overhead_expens']=i.overhead_expens
        dict_finance['file']='pdf'
        dict_finance['total']=i.total
        dict_finance['comment']=i.comment
        dict_finance['subtotal']=i.subtotal
        # print(dict_finance)
        qs_release = ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail,finance_id=i.id)
        qs_uc = UsedBalance.objects.filter(projectpi_id=projectpi_id,projectdetail_id=id_projectdetail,finance_id=i.id)
        qs_release_list = []
        if qs_release:
            for d in qs_release:
                dict_release = {}
                dict_release['id']=d.id
                dict_release['year']=d.year
                dict_release['release_no']=d.release_no
                dict_release['salary']=d.salary
                dict_release['contingencies']=d.contingencies
                dict_release['non_contingencies']=d.non_contingencies
                dict_release['recurring']=d.recurring
                dict_release['travel']=d.travel
                dict_release['overhead_expens']=d.overhead_expens
                dict_release['file']='pdf'
                dict_release['total']=d.total
                dict_release['comment']=d.comment
                dict_release['flag']='rel'
                # print('dict_release',dict_release)
                qs_release_list.append(dict_release)
        if qs_uc:
            for u in qs_uc:
                dict_uc = {}
                dict_uc['id']=u.id
                dict_uc['year']=u.year
                dict_uc['uc_no']=u.uc_no
                dict_uc['salary']=u.salary
                dict_uc['contingencies']=u.contingencies
                dict_uc['non_contingencies']=u.non_contingencies
                dict_uc['recurring']=u.recurring
                dict_uc['travel']=u.travel
                dict_uc['overhead_expens']=u.overhead_expens
                dict_uc['file']='pdf'
                dict_uc['total']=u.total
                dict_uc['interest']=u.interest
                dict_uc['comment']=u.comment
                dict_uc['flag']='uc'
                # print('dict_release',dict_uc)
                qs_release_list.append(dict_uc)
        dict_finance['release']=qs_release_list
        
        qs_list.append(dict_finance)

    print("***********************************************************************")
    # print('qs_list',qs_list)
    return render(request,"account/fund_detail_view.html")

def sansion_year_fetch(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')

    # projectpi_id = request.GET.get('pi_id')
    # id_projectdetail = request.GET.get('project_id')
    # print('pi_id fund_details',projectpi_id)
    # print('project_id fund_details',id_projectdetail)
    qs = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id).values().order_by('year')
    qs_query = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id).order_by('id')
    qs_list = []
    for i in qs_query:
        # print(i.id)
        dict_finance = {}
        dict_finance['id']=i.id
        dict_finance['year']=i.year
        dict_finance['salary']=i.salary
        dict_finance['contingencies']=i.contingencies
        dict_finance['non_contingencies']=i.non_contingencies
        dict_finance['recurring']=i.recurring
        dict_finance['travel']=i.travel
        dict_finance['overhead_expens']=i.overhead_expens
        dict_finance['file']='pdf'
        dict_finance['total']=i.total
        dict_finance['comment']=i.comment
        dict_finance['subtotal']=i.subtotal
        qs_list.append(dict_finance)
    print('qs_list',qs_list)            
    return JsonResponse({'data':list(qs),'newData':qs_list}, safe=False)

def get_releases(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    financial_id = request.GET.get('financial_id')
    qs_release = ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,finance_id=financial_id).values()
    print('qs_list',qs_release)            
    return JsonResponse({'data':list(qs_release)}, safe=False)

def get_uc(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    financial_id = request.GET.get('financial_id')
    qs_uc = UsedBalance.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,finance_id=financial_id).values()
    print('qs_list',qs_uc)            
    return JsonResponse({'data':list(qs_uc)}, safe=False)

def get_balancesheet(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    financial_id = request.GET.get('financial_id')
    qs_balance = BalanceSheet.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,finance_id=financial_id).values()
    # print('qs_balance',qs_balance)            
    return JsonResponse({'data':list(qs_balance)}, safe=False)

def get_unpend_balance(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    financial_year = request.GET.get('year')
    finance_id = request.GET.get('finance_id')
    qs_query = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,year=financial_year).order_by('id')
    print('finance id',qs_query[0].id)
    qs_release = ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,finance_id=finance_id).count()
    print('qs_release count',qs_release)
    qs_balance={}
    if qs_release < 1:
        qs_balance = BalanceSheet.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id,finance_id=qs_query[0].id).values()
        print('qs_balance',qs_balance)            
    return JsonResponse({'data':list(qs_balance),'status':'200 OK'}, safe=False)



def get_balance_sheet(request):
    projectpi_id = request.GET.get('projectpi_id')
    project_id = request.GET.get('project_id')
    dict_list = []
    fields = ['salary', 'contingencies', 'non_contingencies','recurring', 'travel', 'overhead_expens']
    sanction_totals = FinancialDetail.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id).aggregate(**{f: Sum(f) for f in fields})
    dict_list.append(sanction_totals)
    release_total = ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id).aggregate(**{f: Sum(f) for f in fields})
    dict_list.append(release_total)
    uc_total = UsedBalance.objects.filter(projectpi_id=projectpi_id,projectdetail_id=project_id).aggregate(**{f: Sum(f) for f in fields})
    dict_list.append(uc_total)
    unspend = {f: (release_total[f] or 0) - (uc_total[f] or 0) for f in fields}
    dict_list.append(unspend)
    # combined = {f: (sanction_totals[f] or 0) + (release_total[f] or 0) + (uc_total[f] or 0) for f in fields}
    # print('combined***************************************************************',combined)
    keys = list(dict_list[0].keys())            
    return JsonResponse({'data':list(dict_list),"keys": list(keys),'status':'200 OK'}, safe=False)


@login_required(login_url="login")
def senssion_submit(request):
    if request.method == 'POST':
        print('data',request.POST)
        FinancialDetail.objects.create(user=request.user,
                projectpi_id = request.POST['projectpi'],
                projectdetail_id = request.POST['projects'],
                year = request.POST['year'],
                salary = request.POST['salary'],
                contingencies = request.POST['contingencies'],
                non_contingencies = request.POST['noncontingencies'],
                recurring = request.POST['recurring'],
                travel = request.POST['travel'],
                overhead_expens = request.POST['overheadexpens'],
                )
        return JsonResponse({'message':'Form submit successfully!!','status':'200 OK'})
    return JsonResponse({'message':'Form not submitted!!','status':'400 BAD_REQUEST'}) 

def check_release_limit(request):
    
    finance_id = request.GET.get('finance_id')
    sanction = FinancialDetail.objects.get(id=finance_id)
    finance_row = FinancialDetail.objects.filter(id=finance_id).values()
    total_release = sanction.financial_release_detail.count()
    fields = ['salary', 'contingencies', 'non_contingencies', 'recurring', 'travel', 'overhead_expens']
    released_sums = {field: sum(getattr(r, field) for r in sanction.financial_release_detail.all()) for field in fields}
    return JsonResponse({'data':released_sums,'finance_row':list(finance_row),'limit_count':total_release,'status':'200 OK'}, safe=False)

@login_required(login_url="login")
def release_submit(request):
    if request.method == 'POST':
        files = request.FILES.get('uploadfile',None) 
        ReleaseBuget.objects.create(user=request.user,
        finance_id = request.POST['finance_id'],
        projectpi_id = request.POST['projectpi'],
        projectdetail_id = request.POST['projects'],
        year = request.POST['year'],
        salary = request.POST['salary'],
        contingencies = request.POST['contingencies'],
        non_contingencies = request.POST['noncontingencies'],
        recurring = request.POST['recurring'],
        travel = request.POST['travel'],
        overhead_expens = request.POST['overheadexpens'],
        total = request.POST['total'],
        comment = request.POST['comment'],
        fileupload = files,
        )
        return JsonResponse({'message':'Form submit successfully!!','status':'200 OK'})
    return JsonResponse({'message':'Form not submitted!!','status':'400 BAD_REQUEST'}) 
    
@login_required(login_url="login")
def uc_submit(request):
    if request.method == 'POST':
        finance_id = request.POST['finance_id'],
        projectpi_id = request.POST['projectpi'],
        projectdetail_id = request.POST['projects'],
        files = request.FILES.get('uploadfile',None) 
        # print('uc data',request.POST)
        releas_exist=ReleaseBuget.objects.filter(projectpi_id=projectpi_id,projectdetail_id=projectdetail_id,finance_id=finance_id).count()
        uc_exist=UsedBalance.objects.filter(projectpi_id=projectpi_id,projectdetail_id=projectdetail_id,finance_id=finance_id).count()
        # print('releas_exist',releas_exist)
        if releas_exist > 0:
            if uc_exist <= 0:
                UsedBalance.objects.create(user=request.user,
                    finance_id = request.POST['finance_id'],
                    projectpi_id = request.POST['projectpi'],
                    projectdetail_id = request.POST['projects'],
                    year = request.POST['year'],
                    salary = request.POST['salary'],
                    contingencies = request.POST['contingencies'],
                    non_contingencies = request.POST['noncontingencies'],
                    recurring = request.POST['recurring'],
                    travel = request.POST['travel'],
                    overhead_expens = request.POST['overheadexpens'],
                    interest = request.POST['interest'],
                    total = request.POST['total'],
                    comment = request.POST['comment'],
                    fileupload = files,
                )
                # print('data created successfully.')
                return JsonResponse({'message':'Form submit successfully!!','status':'200 OK'})
            else:
                return JsonResponse({'message':'UC can submit only one time!!','status':'400 BAD_REQUEST'})
        else:
            return JsonResponse({'message':'Please first release fund.','status':'400 BAD_REQUEST'})
    return JsonResponse({'message':'Form not submitted!!','status':'400 BAD_REQUEST'})  