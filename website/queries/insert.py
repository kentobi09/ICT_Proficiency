from flask import Blueprint, request,redirect,url_for,flash
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from datetime import datetime
import magic
from sqlalchemy import insert

insert_bp = Blueprint('insert',__name__)

#is_pdf is a function that checks if the uploaded file is a valid pdf only
def is_pdf(applicant_attachment):

    mime = magic.Magic(mime=True)
    applicant_attachment_isValid = applicant_attachment.read(2048)
    applicant_attachment.seek(0)
    return mime.from_buffer(applicant_attachment_isValid) == 'application/pdf'

@insert_bp.route('/',methods = ['POST'])
def insertDiagnosticData():
    if request.method == 'POST':
        applicant_attachment = request.files.get('applicant_attachment')

        if not applicant_attachment or not is_pdf(applicant_attachment):
            flash("Please upload a valid PDF file", 'diagnostic_error')
            return redirect(url_for('views.showDiagnosticTable'))

        diagnostic_form_data = insert(DiagnosticResults).values(
            first_name= request.form['first_name'].strip(),
            middle_name=request.form['middle_name'].strip(),
            last_name=request.form['last_name'].strip(),
            sex=request.form['sex'].strip(),
            province=request.form['province'].strip(),
            exam_venue=request.form['exam_venue'].strip(),
            date_of_examination=datetime.strptime(request.form['date_exam'], '%B %d, %Y').date(),
            date_of_notification=datetime.strptime(request.form['date_notified'],'%B %d, %Y').date(),
            proctor=request.form['proctor'].strip(),
            status=request.form['status'].strip(),
            contact_number=request.form['contact_number'].strip(),
            email_address=request.form['email_address'].strip(),
            part_one_score=request.form['part_one_score'].strip(),
            part_two_score=request.form['part_two_score'].strip(),
            part_three_score=request.form['part_three_score'].strip(),
            total_score=request.form['total_score'],
            applicant_form=applicant_attachment.read()
            )

        db.session.execute(diagnostic_form_data)
        db.session.commit()

        flash("Applicant Record has been inserted successfully", 'diagnostic_success')

    return redirect(url_for('views.showDiagnosticTable'))


@insert_bp.route('/insert_handson',methods = ['POST'])
def insertHandsonData():
    if request.method == 'POST':
        foreign_id = request.form.get('applicant_id')
        isPresentInDiagnostic = DiagnosticResults.query.get(foreign_id)

        if not isPresentInDiagnostic:
            flash("Sorry! Your record is not present in any diagnostic records!", 'handson_error')
            return redirect(url_for('views.showHandsonTable'))

        handson_form_data = insert(HandsonResults).values(
            applicant_id=foreign_id,
            province=request.form.get('province'),
            exam_venue=request.form.get('exam_venue'),
            date_of_examination=datetime.strptime(request.form.get('date_exam', ''), '%B %d, %Y').date(),
            date_of_notification=datetime.strptime(request.form.get('date_notified', ''), '%B %d, %Y').date(),
            proctor=request.form.get('proctor'),
            handson_score=request.form.get('handson_score'),
            status=request.form.get('status')
        )

        db.session.execute(handson_form_data)
        db.session.commit()

        flash("Applicant Record has been inserted successfully", 'handson_success')

    return redirect(url_for('views.showHandsonTable'))
