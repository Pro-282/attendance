from flask import Blueprint, jsonify
from .models import Faculties, Departments, Levels

api = Blueprint('jsons', __name__)

@api.route('api/levels')
def levels():
    levelList=[]
    levels = Levels.query.all()
    for level in levels:
        levelList.append(level.level)
    return jsonify(levelList)
    
@api.route('/api/facs-and-depts')
def faculties():
    response={}
    faculties = Faculties.query.all()
    for faculty in faculties:
        departmentList=[]
        departments = Departments.query.filter_by(faculty_id=faculty.id).all()
        for department in departments:
            departmentList.append(department.department)
        response[faculty.faculty] = [{'id':faculty.id},
                                     {'departments':departmentList}]
    return(jsonify(response))
