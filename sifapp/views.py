from django.shortcuts import render
from django.http import JsonResponse
from odoorpc import ODOO
from . import config

# Create your views here.
odoo = ODOO(config.host,port=config.port)
odoo.login(config.db,config.username,config.password)
employees = odoo.env['hr.employee']

def getEmployees(request):
    db = {}
    employee = employees.search([('status_id','=',1)])
    if employee:
        for e in employee:
            je = employees.browse(e)
            db['title'] = je.title
            db['gender'] = je.gender
            db['email'] = je.email
            db['nationality'] = je.nationality
            db['org_id'] = je.org_id.name
            db['position'] = je.level_id.name
            db['hire_date'] = je.hire_date
            db['date_of_birth'] = je.birthday
            names = je.name_related.split(' ')
            db['last_name'] = names[0].rstrip(',')
            db['first_name'] = names[1].strip()
            db['middle_name'] = names[-1].strip()

    return JsonResponse(db)

def getEmployee(request, employee_no):
    db = {}
    emp = employees.search([('employee_no','=',employee_no)])
    if emp:
        je = employees.browse(emp[0])
        db['title'] = je.title
        db['gender'] = je.gender
        db['email'] = je.email
        db['nationality'] = je.nationality
        db['org_id'] = je.org_id.name
        db['position'] = je.level_id.name
        db['hire_date'] = je.hire_date
        db['date_of_birth'] = je.birthday
        names = je.name_related.split(' ')
        db['last_name'] = names[0].rstrip(',')
        db['first_name'] = names[1].strip()
        db['middle_name'] = names[-1].strip()
        
    return JsonResponse(db)
