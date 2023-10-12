from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



# Display all restaurants.
@app.route('/')
@app.route('/restaurants/')
def showRestaurants(): 
   all_restaurants = session.query(Restaurant).all()
   return render_template('restaurants.html', restaurants=all_restaurants)

# Add a new restaurants.
@app.route('/restaurant/new',methods=['GET', 'POST'])
def newRestaurant(): 
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# Edit an existing restaurant.
@app.route('/restaurant/<int:restaurant_id>/edit' ,methods=['GET', 'POST'])
def editRestaurant(restaurant_id): 
    restaurant_to_edit = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant_to_edit.name = request.form['name']
            # go back to the restaurants page
            return redirect(url_for('showRestaurants'))
    return render_template(
            'editRestaurant.html', restaurant=restaurant_to_edit)

# Delete an existing restaurant.
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant_to_delete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
       session.delete(restaurant_to_delete)
       session.commit()
       return redirect( url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
       return render_template('deleteRestaurant.html', restaurant=restaurant_to_delete)


# Show the restaurant menu.


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id): 
    selected_restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    all_items=session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', items=all_items, restaurant=selected_restaurant)

# Show the restaurant menu. 
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
           newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
           session.add(newItem)
           session.commit()
           return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit the menu item. 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id,menu_id):
    item_to_edit=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if request.form['name']:
            item_to_edit.name = request.form['name']
        if request.form['description']:
            item_to_edit.description = request.form['name']
        if request.form['price']:
            item_to_edit.price = request.form['price']
        if request.form['course']:
            item_to_edit.course = request.form['course']
        session.add(item_to_edit)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item_to_edit)

        


 
 

# Delete the menu item. 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
         session.delete(item_to_delete)
         session.commit()
         return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:     
        return render_template('deletemenuitem.html',item=item_to_delete)

 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)