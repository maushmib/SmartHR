from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # HR URLs
    path('add-teamlead/', views.add_teamlead, name='add_teamlead'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('add-project/', views.add_project, name='add_project'),

    # Task URLs
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('submit-task/<int:task_id>/', views.submit_task, name='submit_task'),
path('approve-task/<int:task_id>/', views.approve_task, name='approve_task'),
   
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('logout/', views.logout_view, name='logout'),
     path('allocate-employees/', views.allocate_employees, name='allocate_employees'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
path('manager-create-project/', views.manager_create_project, name='manager_create_project'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
     path('teamlead/dashboard/', views.teamlead_dashboard, name='teamlead_dashboard'),
    path('teamlead/assign-task/', views.assign_task, name='assign_task'),
    path('teamlead/dashboard/', views.teamlead_dashboard, name='teamlead_dashboard'),
        path('teamlead/choose_project/', views.choose_project, name='choose_project'),
    path('teamlead/create-project/', views.create_project, name='create_project'),
    path('give-rating/', views.give_rating, name='give_rating'),
    path('my-ratings/', views.view_my_ratings, name='my_ratings'),
    path('all-ratings/', views.view_all_ratings, name='all_ratings'),
    path('rating-success/', views.rating_success, name='rating_success'),
    path('resume-match/', views.resume_match_view, name='resume_match'),
    path('upload-resume/', views.upload_resume,name='upload_resume'),
    path('filter/', views.filter_page, name='filter_page'),
    path('filter/results/', views.filter_results, name='filter_results'),
    path('predict/<int:employee_id>/', views.predict_attrition, name='predict_attrition'),
    path('attrition-predict/', views.attrition_prediction_view, name='attrition_prediction'),
   # urls.py
    path('edit-profile/', views.edit_employee_profile, name='edit_employee_profile'),
     path('smart-assign/', views.smart_assign, name='smart_assign'),
   
     path('skill-gap/<int:employee_id>/<int:project_id>/', views.skill_gap_analyzer, name='skill_gap'),
     path("guest/resume-submit/", views.guest_resume_submit, name="guest_resume_submit"),
path("hr/candidates/", views.hr_candidates, name="hr_candidates"),
path("guest/dashboard/", views.guest_dashboard, name="guest_dashboard"),
path('hr/chatbot/', views.HRChatbot.as_view(), name='hr_chatbot'), 
path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
] 



