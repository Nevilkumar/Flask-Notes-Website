from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect
from .models import Note
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note Is Too Short!!!', category='danger')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!!!', category='success')
    return render_template('home.html')


@views.route('/delete-note/', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteid = note['noteid']
    note = Note.query.get(noteid)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
    else:
        return redirect('/')
