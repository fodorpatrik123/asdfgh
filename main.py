import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from models import db, RPAProject
from forms import ProjectForm
from sqlalchemy import or_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpa_projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

def save_file(file_data):
    if file_data:
        filename = secure_filename(file_data.filename)
        # Avoid overwriting or conflicts - simple approach: timestamp or uuid could be added
        # For now, just save.
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_data.save(filepath)
        return filename
    return None

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    missing_docs = request.args.get('missing_docs', '')

    query = RPAProject.query

    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            RPAProject.developer_name.like(search_term),
            RPAProject.requestor.like(search_term)
        ))

    if status_filter:
        query = query.filter(RPAProject.status == status_filter)

    if missing_docs == 'on':
        query = query.filter(or_(
            RPAProject.doc_business == None,
            RPAProject.doc_test == None,
            RPAProject.doc_ops == None,
            RPAProject.doc_business == '',
            RPAProject.doc_test == '',
            RPAProject.doc_ops == ''
        ))

    projects = query.order_by(RPAProject.arrival_date.desc()).all()

    # Get all unique statuses for the filter dropdown
    # Hardcoded or dynamic? Hardcoded in form, so maybe hardcoded here or distinct query.
    # Let's use the list from the form for consistency, or just distinct from DB.
    # Distinct from DB is safer for data integrity but form list is better for UX.
    statuses = ['Új', 'Folyamatban', 'Tesztelés', 'Kész', 'Élesítve', 'Felfüggesztve']

    return render_template('index.html', projects=projects, search=search, status_filter=status_filter, missing_docs=missing_docs, statuses=statuses)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        project = RPAProject(
            developer_name=form.developer_name.data,
            status=form.status.data,
            arrival_date=form.arrival_date.data,
            end_date=form.end_date.data,
            percentage=form.percentage.data,
            fte=form.fte.data,
            requestor=form.requestor.data
        )

        if form.doc_business.data:
            project.doc_business = save_file(form.doc_business.data)
        if form.doc_test.data:
            project.doc_test = save_file(form.doc_test.data)
        if form.doc_ops.data:
            project.doc_ops = save_file(form.doc_ops.data)

        db.session.add(project)
        db.session.commit()
        flash('Projekt sikeresen létrehozva!', 'success')
        return redirect(url_for('index'))
    return render_template('create_edit.html', form=form, title="Új Projekt Felvétele")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    project = RPAProject.query.get_or_404(id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.developer_name = form.developer_name.data
        project.status = form.status.data
        project.arrival_date = form.arrival_date.data
        project.end_date = form.end_date.data
        project.percentage = form.percentage.data
        project.fte = form.fte.data
        project.requestor = form.requestor.data

        # Handle file updates only if new file provided
        if form.doc_business.data:
            project.doc_business = save_file(form.doc_business.data)
        if form.doc_test.data:
            project.doc_test = save_file(form.doc_test.data)
        if form.doc_ops.data:
            project.doc_ops = save_file(form.doc_ops.data)

        db.session.commit()
        flash('Projekt sikeresen frissítve!', 'success')
        return redirect(url_for('index'))

    return render_template('create_edit.html', form=form, title="Projekt Szerkesztése")

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    project = RPAProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Projekt törölve.', 'info')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
