from flask import render_template, flash, redirect,Blueprint, request, url_for, current_app as app,session
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from .models.family_models import FamilyDetails
from .forms.Emp_details import Employee_Details
from .models.emp_detail_models import Employee
from . import db
from datetime import datetime,date
import calendar
from .forms.education import EducationForm,UploadDocForm
from .models.education import Education,UploadDoc
from .forms.family_details import Family_details
from .forms.previous_company import Previous_company
from .models.prev_com import PreviousCompany
from .models.attendance import Punch,LeaveApplication,LeaveBalance
from .forms.attendance import PunchForm,LeaveForm
from .models.manager_model import ManagerContact
from .common import verify_password_and_send_email
from .forms.query_form import PasswordForm



profile=Blueprint('profile',__name__)


@profile.route('/emp_details',methods=['GET','POST'])
@login_required
def emp_profile():
    form=Employee_Details()
    return render_template("profile/emp_det.html",form=form)


@profile.route('/emp_det2', methods=['GET', 'POST'])
@login_required
def empl_det():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    form = Employee_Details(obj=employee) 
    
    if form.validate_on_submit():
        # Check if a file is uploaded
        if form.Photo.data:
            # Get the file size
            file = form.Photo.data
            file_size = file.content_length  # Get the file size in bytes
            
            # Check if file size exceeds 100 KB (102400 bytes)
            if file_size > 102400:  # 100 KB
                flash('File size exceeds 100 KB. Please upload a smaller file.', 'warning')
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Continue processing...
                if employee:
                    form.populate_obj(employee)
                    employee.photo_filename = filename
                    db.session.commit()
                    flash('Employee details updated successfully!', 'success')
                else:
                    new_employee = Employee(
                        admin_id=current_user.id, 
                        photo_filename=filename,
                        name=form.name.data,
                        email=form.email.data,
                        father_name=form.father_name.data,
                        mother_name=form.mother_name.data,
                        marital_status=form.marital_status.data,
                        spouse_name=form.spouse_name.data,
                        dob=form.dob.data,
                        emp_id=form.emp_id.data,
                        designation=form.designation.data,
                        mobile=form.mobile.data,
                        gender=form.gender.data,
                        emergency_mobile=form.emergency_mobile.data,
                        caste=form.caste.data,
                        nationality=form.nationality.data,
                        language=form.language.data,
                        religion=form.religion.data,
                        blood_group=form.blood_group.data,
                        permanent_address_line1=form.permanent_address_line1.data,
                        permanent_address_line2=form.permanent_address_line2.data,
                        permanent_address_line3=form.permanent_address_line3.data,
                        permanent_pincode=form.permanent_pincode.data,
                        permanent_district=form.permanent_district.data,
                        permanent_state=form.permanent_state.data,
                        present_address_line1=form.present_address_line1.data,
                        present_address_line2=form.present_address_line2.data,
                        present_address_line3=form.present_address_line3.data,
                        present_pincode=form.present_pincode.data,
                        present_district=form.present_district.data,
                        present_state=form.present_state.data
                    )
                    db.session.add(new_employee)
                    db.session.commit()
                    flash('Employee details saved successfully!', 'success')
        else:
            # Handle case where no file was uploaded
            flash('No photo was uploaded. Please upload a photo.', 'warning')
        
        return redirect(url_for('profile.empl_det'))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')
    
    return render_template('profile/emp_det.html', form=form)





@profile.route('/family_det')
@login_required
def fam_det():
    family_members = FamilyDetails.query.filter_by(admin_id=current_user.id).all()
    return render_template('profile/E_Family_details.html',family_members = family_members)





@profile.route('/family_details', methods=['GET', 'POST'])
@login_required
def family_details():
    form = Family_details()
    
    if form.validate_on_submit():
        photo_filename = None
        if form.Photo.data:
            photo_filename = secure_filename(form.Photo.data.filename)
            form.Photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        new_family_member = FamilyDetails(
            admin_id=current_user.id,
            photo_filename=photo_filename,
            name=form.name.data,
            email=form.email.data,
            dob=form.dob.data,
            age=int(form.age.data),
            relation=form.relation.data,
            occupation=form.occupation.data,
            income=form.Income.data,
            address=form.Address.data,
            remarks  =form.Remarks.data,
            
        )
        
        db.session.add(new_family_member)
        db.session.commit()
        
        flash('Family member details saved successfully!', 'success')
        return redirect(url_for('profile.fam_det'))
   
    return render_template('profile/form_E_FAM.html', form=form)





@profile.route('/previous_company', methods=['GET', 'POST'])
@login_required
def previous_company():
    form = Previous_company()
    if form.validate_on_submit():
        new_company = PreviousCompany(
            admin_id=current_user.id,
            com_name=form.com_name.data,
            designation=form.designation.data,
            doj=form.doj.data,
            dol=form.dol.data,
            reason=form.reason.data,
            salary=form.salary.data,
            uan=form.uan.data,
            pan=form.pan.data,
            contact=form.contact.data,
            name_contact=form.name_contact.data,
            pf_num=form.pf_num.data,
            address=form.address.data
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Previous company details saved successfully!', 'success')
        return redirect(url_for('profile.previous_company'))

    previous_companies = PreviousCompany.query.filter_by(admin_id=current_user.id).all()
    return render_template('profile/previous_company.html', form=form, previous_companies=previous_companies)




@profile.route('/education', methods=['GET', 'POST'])
@login_required
def education():
    form = EducationForm()
    education = Education.query.filter_by(admin_id=current_user.id).all()

    if form.validate_on_submit():
        if form.doc_file.data:
            filename = secure_filename(form.doc_file.data.filename)
            form.doc_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_education = Education(
            admin_id=current_user.id,
            qualification=form.qualification.data,
            institution=form.institution.data,
            board=form.board.data,
            start=form.start.data,
            end=form.end.data,
            marks=form.marks.data,
            doc_file=filename
        )
        db.session.add(new_education)
        db.session.commit()
        flash('Education details added successfully!', 'success')
        return redirect(url_for('profile.education'))

    return render_template('profile/education.html', form=form, education=education)





@profile.route('/delete_education/<int:education_id>', methods=['POST'])
@login_required
def delete_education(education_id):
    education = Education.query.get_or_404(education_id)
    if education.admin_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('profile.education'))
    
    db.session.delete(education)
    db.session.commit()
    flash('Education detail deleted successfully!', 'success')
    return redirect(url_for('profile.education'))





@profile.route('/upload_doc', methods=['GET', 'POST'])
@login_required
def upload_docs():
    form = UploadDocForm()
    upload_doc = UploadDoc.query.filter_by(admin_id=current_user.id).all()

    if form.validate_on_submit():
        if form.doc_file.data:
            filename = secure_filename(form.doc_file.data.filename)
            form.doc_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_upload_doc = UploadDoc(
            admin_id=current_user.id,
            doc_name=form.doc_name.data,
            doc_number=form.doc_number.data,
            issue_date=form.issue_date.data,
            doc_file=filename
        )
        db.session.add(new_upload_doc)
        db.session.commit()
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('profile.upload_docs'))

    return render_template('profile/upload_doc.html', form=form, upload_doc=upload_doc)





@profile.route('/delete_document/<int:doc_id>', methods=['POST'])
@login_required
def delete_document(doc_id):
    document = UploadDoc.query.get_or_404(doc_id)
    if document.admin_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('profile.upload_docs'))
    
   
    if document.doc_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.doc_file)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(document)
    db.session.commit()
    flash('Document deleted successfully!', 'success')
    return redirect(url_for('profile.upload_docs'))




@profile.route('/punch', methods=['GET', 'POST'])
@login_required
def punch():
    form = PunchForm()

    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()
    selected_month = request.args.get('month', today.month, type=int)
    selected_year = request.args.get('year', today.year, type=int)

   
    calendar.setfirstweekday(calendar.MONDAY)

    first_day = date(selected_year, selected_month, 1)
    last_day = first_day.replace(day=calendar.monthrange(selected_year, selected_month)[1])

    punches = Punch.query.filter(
        Punch.admin_id == current_user.id,
        Punch.punch_date.between(first_day, last_day)
    ).all()

    punch_data = {p.punch_date: p for p in punches}

    if form.validate_on_submit():
        if form.punch_in.data:
            if punch and punch.punch_in:
                flash('Already punched in today!', 'danger')
            else:
                if not punch:
                    punch = Punch(admin_id=current_user.id, punch_date=today)
                punch.punch_in = datetime.now().time()
                db.session.add(punch)
                db.session.commit()
                flash('Punched in successfully!', 'warning')

        elif form.punch_out.data:
            if not punch or not punch.punch_in:
                flash('You need to punch in first!', 'danger')
            else:
                punch.punch_out = datetime.now().time()
                db.session.commit()
                flash('Punch out time updated successfully!', 'success')

    return render_template('profile/punch.html', form=form, punch=punch, punch_data=punch_data, today=today, selected_month=selected_month, selected_year=selected_year, calendar=calendar)





@profile.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    form = LeaveForm()
    password_form = PasswordForm()
    leave_balance = LeaveBalance.query.filter_by(admin_id=current_user.id).first()

    
    if 'leave_data' in session and password_form.validate_on_submit():
        leave_data = session.pop('leave_data')

       
        start_date = datetime.strptime(leave_data['start_date'], '%a, %d %b %Y %H:%M:%S %Z').date()
        end_date = datetime.strptime(leave_data['end_date'], '%a, %d %b %Y %H:%M:%S %Z').date()

        leave_type = leave_data['leave_type']
        leave_days = (end_date - start_date).days + 1

       
        if leave_type == 'Casual Leave':
            if leave_days > 2:
                flash('Casual leave cannot exceed 2 days.', 'danger')
                return redirect(url_for('profile.apply_leave'))

            if leave_days > leave_balance.casual_leave_balance:
                flash('You do not have enough Casual leave, Try Privilege Leave.', 'danger')
                return redirect(url_for('profile.apply_leave'))
            else:
                leave_balance.casual_leave_balance -= leave_days

    
        elif leave_type == 'Privilege Leave':
            if leave_days > leave_balance.privilege_leave_balance:
                extra = leave_days - leave_balance.privilege_leave_balance
                leave_balance.privilege_leave_balance = leave_balance.privilege_leave_balance % 1
            else:
                leave_balance.privilege_leave_balance -= leave_days
            


       
        leave_application = LeaveApplication(
            admin_id=leave_data['admin_id'],
            leave_type=leave_data['leave_type'],
            reason=leave_data['reason'],
            start_date=start_date,
            end_date=end_date,
            status='Pending'
        )

        db.session.add(leave_application)
        db.session.commit()

        approval_link = url_for('profile.approve_leave', leave_id=leave_application.id, _external=True)



       
        manager_contact = ManagerContact.query.filter_by(circle_name=current_user.circle, user_type=current_user.Emp_type).first()
        department_email = 'hr@saffotech.com'
        cc_emails = ['accounts@saffotech.com']

        if manager_contact:
            cc_emails += [manager_contact.l2_email, manager_contact.l3_email]

        
        subject = f"New Leave Application Submitted: {leave_application.leave_type}"
        body = (
            f"Leave application has been submitted by {current_user.first_name}.\n"
            f"Leave Type: {leave_application.leave_type}\n\n"
            f"Reason: {leave_application.reason}\n\n"
            f'Extra Days: {extra}\n\n'
            f"Start Date: {leave_application.start_date}\n"
            f"End Date: {leave_application.end_date}\n"
            f" Total Leave {leave_days}\n\n"
            f"Also click on link to Approve : { approval_link } "

           
        )

        if verify_password_and_send_email(current_user, password_form.password.data, subject, body, department_email, cc_emails):
            flash('Your leave application has been submitted and email notification sent to the department.', 'success')
        else:
            flash('Password verification failed or email could not be sent.', 'error')

        return redirect(url_for('profile.apply_leave'))

    
    if form.validate_on_submit():
       
        session['leave_data'] = {
            'admin_id': current_user.id,
            'leave_type': form.leave_type.data,
            'reason': form.reason.data,
            'start_date': form.start_date.data, 
            'end_date': form.end_date.data,
        }

        
        return render_template('Accounts/verify_password.html', form=password_form)

    
    leave = LeaveApplication.query.filter_by(admin_id=current_user.id).all()

    return render_template('profile/apply_leave.html', form=form, leave_balance=leave_balance, user_leaves=leave)


@profile.route('/approve-leave/<int:leave_id>', methods=['GET'])
def approve_leave(leave_id):
    leave_application = LeaveApplication.query.get_or_404(leave_id)

    
    leave_application.status = 'Approved'
    db.session.commit()

    
    return """
        <h1>Leave application has been approved.</h1>
        <p>Thank you for approving the leave application. The status has been updated successfully.</p>
    """


  
    






