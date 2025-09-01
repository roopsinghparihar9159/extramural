from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import  ProjectPIDetail, ProjectDetail,FinancialDetail,InstituteDetail,District,State,ReleaseBuget,UsedBalance
from account.forms import ProjectPIDetailForm, ProjectDetailForm, FinancialDetailForm,InstituteDetailForm
import os
import json
import datetime
from datetime import datetime
# Create your views here.
@login_required(login_url="login")
def home(request):

    return render(request,'account/home.html')

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
    print(request.POST)
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

def get_states(request):
    institute_id = request.GET.get('institute_id')
    institute_obj = InstituteDetail.objects.filter(id=institute_id).first()
    states = State.objects.filter(id=institute_obj.state_id).values('id', 'name')
    return JsonResponse(list(states), safe=False)

def get_districts(request):
    institute_id = request.GET.get('institute_id')
    institute_obj = InstituteDetail.objects.filter(id=institute_id).first()

    districts = District.objects.filter(id=institute_obj.district_id).values('id', 'name')
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
        # files  = request.FILES
        # print('files',files[0])
        # print('json_data',len(json_data))
        for row in return_data:
            # print(row['id'])
            # print(row['projectpi_id'])
            # print(row['projects_id'])
            # print(row['inputs']['year_row'])
            # print(row['inputs']['salary_row'])
            # print(row['inputs']['contingencies_row'])
            # print(row['inputs']['noncontingencies_row'])
            # print(row['inputs']['recurring_row'])
            # print(row['inputs']['travel_row'])
            # print(row['inputs']['overhead_row'])
            # print(row['inputs']['amt'])
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
               
        # for i in range(0,len(return_data)):
        #     print(i)
        #     idexist = return_data[i]['id']
            # print(return_data[i])
            # print('id',return_data[i]['id'])
            # print(return_data[i]['inputs']['year_row'])
            # print(return_data[i]['inputs']['salary_row'])
            # print('projectpi_id',return_data[i]['projectpi_id'])
            # print('projects_id',return_data[i]['projects_id'])
            # print(return_data[i]['inputs']["file[]"])
            # print(request.FILES.get(return_data[i]['inputs']["file[]"]))
            
            # FinancialDetail.objects.create(user=request.user,
            # projectpi_id = json_data[i]['projectpi_id'],
            # projectdetail_id = json_data[i]['projects_id'],
            # year = json_data[i]['year'],
            # salary = json_data[i]['salary'],
            # contingencies = json_data[i]['contingencies'],
            # non_contingencies = json_data[i]['noncontingencies'],
            # recurring = json_data[i]['recurring'],
            # travel = json_data[i]['travel'],
            # overhead_expens = json_data[i]['overhead'],
            # total = 100,
            # fileupload = files[i],
            # )
            # if idexist != '000':
            #     print(" Record already exists going for update mode")
            # else:
                # FinancialDetail.objects.create(user=request.user,
                # projectpi_id = return_data[i]['projectpi_id'],
                # projectdetail_id = return_data[i]['projects_id'],
                # year = return_data[i]['inputs']['year_row'],
                # salary = return_data[i]['inputs']['salary_row'],
                # contingencies = return_data[i]['inputs']['contingencies_row'],
                # non_contingencies = return_data[i]['inputs']['noncontingencies_row'],
                # recurring = return_data[i]['inputs']['recurring_row'],
                # travel = return_data[i]['inputs']['travel_row'],
                # overhead_expens = return_data[i]['inputs']['overhead_row'],
                # total = return_data[i]['inputs']['amt'],
                # fileupload = return_data[i]['inputs']['file'],
                # )
                # print(return_data[i]['inputs']['year_row'])
                # print('Record is not exist going to create mode')    

        
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