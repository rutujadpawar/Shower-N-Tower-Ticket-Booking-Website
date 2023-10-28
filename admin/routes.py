from flask import render_template,session, request,redirect,url_for,flash
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Brand
from shop.customers.model import Register,CustomerOrder

@app.route('/admin')
def admin():
    products = Addproduct.query.all()
    return render_template('admin/index.html',products=products)

@app.route('/logout')
def admin_logout():
    #logout_user()
    return redirect(url_for('home'))

@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', brands=brands)


@app.route('/categories')
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',categories=categories)

@app.route('/userorders')
def userorders():
    allorders = CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    return render_template('admin/userorders.html', allorders=allorders)


@app.route('/userindorder/<invoice>')
def userindorder(invoice):
    grandTotal = 0
    subTotal = 0
    orders = CustomerOrder.query.filter_by(invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    customer = Register.query.filter_by(id=orders.customer_id).first()
    for _key, product in orders.orders.items():
        discount = (product['discount']/100) * float(product['price'])
        subTotal += float(product['price']) * int(product['quantity'])
        subTotal -= discount
        tax = ("%.2f" % (.06 * float(subTotal)))
        grandTotal = ("%.2f" % (1.06 * float(subTotal)))
    return render_template('admin/userindorder.html', invoice=invoice,customer=customer, tax=tax,subTotal=subTotal,grandTotal=grandTotal,orders=orders)


@app.route('/users')
def users():
    allusers = Register.query.order_by(Register.id.desc()).all()
    return render_template('admin/users.html', allusers=allusers)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} you are logedin now','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Wrong email and password', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)