from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.loginpage, name="login"),
    path('logout/', views.logoutview, name="logout"),
    path("loginview/",views.loginview,name="loginview"),
    path("projectentry/",views.projectentry,name="projectentry"),
    path('load-districts/', views.load_districts, name='load_districts'),
    path('pidetailsave/', views.pidetailsave, name='pidetailsave'),
    path('proejct_detailsave/', views.proejct_detailsave, name='proejct_detailsave'),
    path('institute/', views.institute_detailsave, name='institute'),
    path('filter_project/', views.filter_project, name='filter_project'),
    path('financial/', views.financial_save, name='financial'),
    path('financial_record/', views.fetch_financial_record, name='financial_record'),
    path('financial_save/', views.financial_save_record, name='financial_save'),
    path('release_save/', views.release_save_record, name='release_save'),
    path('uc_save/', views.uc_save_record, name='uc_save'),
    path('filter_projectdetail/', views.filter_projectdetail, name='filter_projectdetail'),
    path('filter_pi_project/', views.filter_pi_project, name='filter_pi_project'),

    path('ajax/get-states/', views.get_states, name='get_states'),
    path('ajax/get-districts/', views.get_districts, name='get_districts'),
    path('autocomplete_area_experties/', views.autocomplete_area_experties, name='autocomplete_area_experties'),
    path('autocomplete_designation/', views.autocomplete_designation, name='autocomplete_designation'),

    # project views urls
    path("projectview/",views.projectview,name="projectview"),
    path("project_detail_view/<int:pk>/",views.project_detail_view,name="project_detail_view"),
    path("pi_detail_view/<int:pk>/",views.pi_detail_view,name="pi_detail_view"),
    path("fund_details/",views.fund_details,name="fund_details"),
    path("sansion_year_fetch/",views.sansion_year_fetch,name="sansion_year_fetch"),
    path('get-releases/', views.get_releases, name='get_releases'),
    path('get_uc/', views.get_uc, name='get_uc'),
    path('get_balance/',views.get_balancesheet,name="get_balance"),
    path('get_unpend_balance/',views.get_unpend_balance,name="get_unpend_balance"),
    path('get_balance_sheet/',views.get_balance_sheet,name="get_balance_sheet"),

    path('senssion_submit/',views.senssion_submit,name="senssion_submit"),
    path('check_release_limit/',views.check_release_limit,name="check_release_limit"),
    path('release_submit/',views.release_submit,name="release_submit"),
    path('uc_submit/',views.uc_submit,name="uc_submit"),
    
]
