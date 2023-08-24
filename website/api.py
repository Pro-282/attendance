from flask import Blueprint, jsonify, request
from .models import Faculties, Departments, Levels, Students
from dependencies.dependent import db
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

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

@api.route('/api/enroll-fingerprint', methods=['GET', 'POST'])
def enroll():
    data = request.get_json()
    matric_no = data.get('matric_no')
    user=Students.query.filter_by(matric_no=matric_no).first()
    print(user.finger_id)
    print(user.matric_no)
    print(user.first_name)

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return jsonify({"message": "Fingerprint sensor not found", "error": str(e)})

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return jsonify({"message": "Your fingerprint exists already", "position": positionNumber})

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(FINGERPRINT_CHARBUFFER2)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

        user.finger_id = positionNumber;
        db.session.commit()

        return jsonify({"message": "Fingerprint enrolled successfully", "position": positionNumber})

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return jsonify({"message": "Enrollment failed", "error": str(e)})