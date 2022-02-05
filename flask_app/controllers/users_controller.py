from flask_app import app, bcrypt
from flask import render_template, request, redirect, session
from flask_app.models.user_model import User

@app.route('/users/new')
def new_user():
    if 'uuid' in session:
        return redirect('/')
    return render_template('create_user.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    if not User.validate_reg(request.form):
        return redirect('/users/new')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        ** request.form,
        'password': pw_hash
    }
    user_id = User.create(data)
    session['uuid'] = user_id
    return redirect('/')

# @app.route('/users/<int:id>')
# def show_user(id):
#     user = User.get_one({'id': id})
#     return render_template('show_user.html', user=user)

# @app.route('/users/<int:id>/edit')
# def edit_user(id):
#     user = User.get_one({'id': id})
#     return render_template('edit_user.html', user=user)

# @app.route('/users/<int:id>/update', methods=['POST'])
# def update_user(id):
#     data = {
#         **request.form,
#         'id': id
#     }
#     User.update_one(data)
#     return redirect(f'/users/{id}')

# @app.route('/users/<int:id>/delete')
# def delete_user(id):
#     User.delete_one({'id': id})
#     return redirect('/users')

@app.route('/users/login', methods=['POST'])
def user_login():
    is_valid = User.validate_login(request.form)
    if not is_valid:
        return redirect('/users/new')
    return redirect('/')

@app.route('/users/logout')
def logout():
    session.pop('uuid')
    return redirect('/')