from django.shortcuts import render
from django.http import HttpResponse
from odoorpc import ODOO
from . import config
import json

# Create your views here.
odoo = ODOO(config.host,port=config.port)
odoo.login(config.db,config.username,config.password)
employees = odoo.env['hr.employee']

def getEmployees(request):
    db = {}
    alldb = []
    employee = employees.search([('status_id','=',1)])
    if employee:
        for e in employee:
            je = employees.browse(e)
            db['emp_num'] = je.employee_no
            #db['title'] = je.title
            db['gender'] = je.gender
            db['email'] = je.work_email
            db['nationality'] = True
            db['org_id'] = je.lga_id.name
            db['position'] = je.level_id.name
            db['hire_date'] = je.hire_date.strftime('Y-%m-%%d') if je.hire_date else False
            db['date_of_birth'] = je.birthday.strftime('%Y-%m-%d') if je.birthday else False
            names = je.name_related.split(' ')
            if len(names) == 3:
                db['last_name'] = names[0].rstrip()
                db['first_name'] = names[1].strip()
                db['middle_name'] = names[-1].strip()
            if len(names) == 2:
                db['last_name'] = names[0].strip()
                db['first_name'] = names[-1].strip()
            alldb.append(db)

    return HttpResponse(json.dumps(alldb), content_type='application/javascript; charset=utf8')

def getEmployee(request, employee_no):
    db = {}
    emp = employees.search([('employee_no','=',employee_no)])
    if emp:
        je = employees.browse(emp[0])
        db['emp_num'] = je.employee_no
        #db['title'] = je.title
        db['gender'] = je.gender
        db['email'] = je.work_email
        db['nationality'] = True
        db['org_id'] = je.lga_id.name
        db['position'] = je.level_id.name
        db['hire_date'] = je.hire_date.strftime('%Y-%m-%d')
        db['date_of_birth'] = je.birthday.strftime('%Y-%m-%d')
        names = je.name_related.split(' ')
        if len(names) == 3:
            db['last_name'] = names[0].rstrip(',')
            db['first_name'] = names[1].strip()
            db['middle_name'] = names[-1].strip()
        if len(names) == 2:
            db['last_name'] = names[0].strip()
            db['first_name'] = names[-1].strip()
    alldb = json.dumps(db)
        
    return HttpResponse(alldb, content_type='application/javascript; charset=utf8')
