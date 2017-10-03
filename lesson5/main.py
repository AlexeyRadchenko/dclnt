from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///Products.db')
metadata = MetaData(bind=engine)
products_table = Table('product', metadata, autoload=True)

app = Flask(__name__)
app.static_url_path = 'static'


@app.route('/')
def product_list():
    products_list = products_table.select().execute().fetchall()
    products = [dict(zip(product.keys(), product)) for product in products_list]
    return render_template('product_list.html', products=products)


@app.route('/product/<product_id>')
def product(product_id):
    product_item = products_table.select().where('id = '+product_id).execute().fetchone()
    product = dict(zip(product_item.keys(), product_item))
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)