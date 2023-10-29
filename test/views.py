## Define url - routes and views for application

from test import app, db, socketio, jwt, bcrypt
from flask import render_template, redirect, request
from flask import flash, url_for, jsonify, session
from flask_jwt_extended import create_access_token, set_access_cookies

from test.forms import RegistrationForm, LoginForm, TaskForm, UpdateForm
from test.models import User, Task
from test.middleware import auth, guest


@app.route('/dashboard/<int:id>', methods=['GET', 'POST'])
@app.route('/')
@auth
def dashboard(id):

    ## Get the form from Taskform
    form = TaskForm(request.form)

    ## Fetch user & task information.
    user = User.query.filter_by(email=session['email']).first()

    ## fetch task data
    if user.is_admin:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id = user.id).all()

    return render_template('dashboard.html', user=user, tasks=tasks, form=form)


@app.route('/logout')
@auth
def logout():
    session.pop('email', None)
    return redirect('login')


### Define page route to create an account
@app.route('/register', methods=['GET', 'POST'])
@guest
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Account already exists! Try login or use different email address.', 'primary')
            return redirect(url_for('login'))
        
        else:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(fullname = form.fullname.data,
                        username = form.username.data,
                        password = hashed_pw,
                        email = form.email.data,
                        is_admin = form.admin.data,
                        role = form.role.data)

            ## add new user to database.
            db.session.add(user)
            db.session.commit()

            flash('Your account has been created! Login to use application', 'success')

            return redirect(url_for('login'))

    return render_template('register.html', title='Create account ', form=form)


### Define login route 
@app.route('/login', methods=['GET', 'POST'])
@guest
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        authenticated = user and bcrypt.check_password_hash(user.password, form.password.data)

        if authenticated:
            if user.is_admin:
                access_token = create_access_token(user.email)
                set_access_cookies(jsonify({'message': 'You are logged in as admin'}), access_token)

                ## Admin user
                session['email'] = user.email
                return redirect(url_for('dashboard', id=user.id))

            else:
                ## Regular user
                flash('Login Successfully', 'success')
                session['email'] = user.email
                return redirect(url_for('dashboard', id=user.id))

        else:
            if not user:
                flash('Account does not exists for this email. Create an acoount first', 'danger')
                return redirect(url_for('login'))
            else:
                flash('Login Unsuccessful! Please check email and password.', 'danger')
                return redirect(url_for('login'))
    
    return render_template('login.html', title='Sign in to your account', form=form)


### Add task
@app.route('/add_task', methods=['GET', 'POST'])
@auth
def add_task():

    user = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        form = TaskForm(request.form)
        task = Task(name=form.name.data, status=form.status.data, due_date=form.due_date.data, user_id=user.id)
        
        ## add new todo task to database.
        db.session.add(task)
        db.session.commit()
    
        flash(f'New task added successfully', 'primary')
        return redirect(url_for('dashboard', id=user.id))
        
    return redirect(url_for('dashboard', id=user.id))

### update task
@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@auth
def update_task(task_id):

    user = User.query.filter_by(email=session['email']).first()
     
    if request.method == 'POST':
        form = UpdateForm(request.form)
        task = Task.query.get(task_id)
        if task:
            task.name = form.name.data
            task.status = form.status.data

            ## Update database
            db.session.commit()
            flash('Task updated successfully')
            return redirect(url_for('dashboard', id=user.id))
        
    return redirect(url_for('dashboard', id=user.id))
    

## Delete task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
@auth
def delete_task(task_id):
        task = Task.query.get(task_id)

        if task:
            ## add new todo task to database.
            db.session.delete(task)
            db.session.commit()

        user = User.query.filter_by(id=task.user_id).first()

        flash(f'One task deleted sucessfully by {user.fullname}', 'danger')
        return redirect(url_for('dashboard', id=user.id))

