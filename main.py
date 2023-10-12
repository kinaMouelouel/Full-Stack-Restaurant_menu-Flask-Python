from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# Display all restaurants.
@app.route('/')
@app.route('/restaurants/')
def showRestaurants(): 
   return render_template('restaurants.html', restaurants=restaurants)

# Add a new restaurants.
@app.route('/restaurant/new')
def newRestaurant(): 
    return render_template('newRestaurant.html')

# Edit an existing restaurant.
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id): 
    return render_template(
            'editRestaurant.html', restaurant=restaurant)

# Delete an existing restaurant.
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id): 
  return render_template('deleteRestaurant.html', restaurant=restaurant)


# Show the restaurant menu.


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id): 
    return render_template('menu.html', items=items, restaurant=restaurant)

# Show the restaurant menu. 
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):     
    return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit the menu item. 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id): 
 return render_template('editmenuitem.html',item=item)

# Delete the menu item. 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id): 
    return render_template('deletemenuitem.html',item=item)

 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)