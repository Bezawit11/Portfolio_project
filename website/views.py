from flask import Blueprint, render_template, request, session, redirect, flash
from . models import User, Item, Order, Cart
from flask_login import login_required, current_user
from . import db
import re, datetime
from .form import AdminForm

app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def home():
    return render_template('home.html')

@app_views.route('/items')
@login_required
def list_items():
    items = []
    categories = []
    all_items = Item.query.filter_by(out_of_stock=False).all()
    for i in all_items:
        if i.category not in categories:
            categories.append(i.category)
        items.append(i)
    return render_template('items.html', items=items, categories=categories)

@app_views.route('/app_admins')
@login_required
def admin():
    return render_template('admin.html')

@app_views.route('/add-items', methods=['GET', 'POST'])
@login_required
def NewItem():
    form = AdminForm()
    if form.validate_on_submit():
        item1 = Item.query.filter_by(name=form.item_name.data.capitalize(), category=form.category.data).first()
        if item1:
            item1.price = form.price.data
            item1.out_of_stock = False
            db.session.commit()
            flash('Item updated')
            return redirect('/add-items')
        else:
            item1 = Item(name=form.item_name.data.capitalize(), price=form.price.data, category=form.category.data, out_of_stock=False)
            db.session.add(item1)
            db.session.commit()
            return redirect('/items')
    return render_template('additem.html', form=form)
    
@app_views.route('/remove-items', methods=['GET', 'POST'])
@login_required
def RemoveItem():
    if request.method == 'POST':
        n = request.form['itemname'].capitalize()
        item = Item.query.filter_by(name=n).first()   
        if item:
            cart = Cart.query.filter_by(item_id=item.id).first()
            if cart:
                db.session.delete(cart)
                db.session.commit()
            item.out_of_stock = True
            db.session.commit()
            return redirect('/items')
    return render_template('removeitem.html')

@app_views.route('/search', methods=['GET', 'POST'])
@login_required
def searched():
    result = []
    categories = []
    n = request.form['searched_name']
    res = Item.query.all()
    for i in res:
        if re.search(n.lower(), i.name.lower()): #re.search(i.name.lower(), n.lower()) or
            result.append(i)
        if i.category not in categories:
            categories.append(i.category)
    return render_template('items.html', items=result, categories=categories)

@app_views.route('/in_cart', methods=['GET', 'POST'])
@login_required
def added_to_cart():
    items_id = request.form['orderz']
    item_quantity = request.form['quantity']
    try: 
        if float(item_quantity) != 0:
            check = Cart.query.filter_by(item_id=items_id, user_id=current_user.get_id()).first()
            if check is not None:
                check.quantity += float(item_quantity)
                db.session.commit()
            else:
                cart1 = Cart(item_id=items_id, user_id=current_user.get_id(), quantity=item_quantity)
                db.session.add(cart1)
                db.session.commit()
        return redirect("/items")
    except:
        flash("Input amount correctly")
        return redirect("/items")

@app_views.route('/show-cart', methods=['GET', 'POST'])
@login_required
def show_my_cart():
    l = []
    total_price = 0
    all_cart = Cart.query.filter_by(user_id=current_user.get_id()).all()
    for k in all_cart:
        l.append(k)
        total_price += k.item.price * k.quantity
    return render_template("cart.html", cart=l, price=total_price)


@app_views.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    if request.method == 'POST' and 'phone_number' in request.form and 'address' in request.form:
        address = request.form['address']
        contact_number = request.form['phone_number']
        all_cart = Cart.query.filter_by(user_id=current_user.get_id()).all()
        for j in all_cart:
            order1 = Order(amount=j.quantity, date=datetime.datetime.now(), address=address, contact_number=contact_number, item_id=j.item.id, user_id=current_user.id)
            #item1 = Item.query.filter_by(id=j.item.id).first()
            db.session.add(order1)
            db.session.commit()
            db.session.delete(j)
            db.session.commit()
            #db.session.delete(item1)
            #db.session.commit()
        return redirect('/items')
    return render_template('order.html')

@app_views.route('/category/<category>', methods=['GET', 'POST'])
@login_required
def list_by_category(category):
    items = []
    categories = []
    if category == "all":
        return redirect("/items")
    specified_items = Item.query.filter_by(category=category).all()
    all_items = Item.query.all()
    for i in specified_items:
        #orders = Order.query.filter_by(item_id=i.id).first()
        #if not orders:
        items.append(i)
    for a in all_items:
        if a.category not in categories:
            categories.append(a.category)
    return render_template('items.html', items=items, categories=categories, listOf=category)

@app_views.route('/cancel-order', methods=['GET', 'POST'])
@login_required
def cancels_order():
    ItemId = request.form['cancel']
    cart1 = Cart.query.filter_by(item_id=ItemId).first()
    db.session.delete(cart1)
    db.session.commit()
    return redirect("/show-cart")

@app_views.route('/view-history', methods=['GET', 'POST'])
@login_required
def show_order_history():
    total_price = 0
    all_orders = Order.query.filter_by(user_id=current_user.id).all()
    for i in all_orders:
        total_price += i.order_price()
    return render_template('history.html', all_orders=all_orders, total_price=total_price)


