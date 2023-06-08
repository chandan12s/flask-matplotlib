import base64
import plotly.graph_objects as go
import io
from flask import Flask, render_template, request, redirect, url_for
from matplotlib import pyplot as plt
import mysql.connector

def connectToDatabase(user,password,host,database):
    mydb = mysql.connector.connect(
        user="root",
        password="spearmeroman",
        host="localhost",
        database="wiley_practice"
    )
    return mydb

def fetchFromDatabase(mydb,query):
    # fetching data from the database
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult

def createApp():
    # creating a flask application
    app = Flask(__name__)
    mydb = connectToDatabase("root","root","localhost","c361")
    create_query = "CREATE TABLE IF NOT EXISTS fruits (id INT AUTO_INCREMENT PRIMARY KEY, fruit_name VARCHAR(255), quantity INT)"
    insert_query = "insert into fruits (fruit_name,quantity) values (%s,%s)"
    search_query = "select * from fruits where fruit_name = %s"
    mycursor = mydb.cursor()


    # this function will simply fetch data from db and display it on homepage
    @app.route('/')
    def index():
        mycursor.execute(create_query)
        myresult = fetchFromDatabase(mydb,"SELECT * FROM fruits")
        return render_template("index.html", data=myresult)
    

    # creating a route to insert data into the database using a form
    @app.route('/insert', methods=['GET','POST'])
    def insert():
        if request.method == 'POST':
            fruit_name = request.form['fruit_name']
            quantity = request.form['quantity']
            val = (fruit_name,quantity)
            mycursor.execute(insert_query,val)
            mydb.commit()
            return redirect(url_for('index'))
        return render_template("insert.html")
    
    @app.route('/plot', methods=['GET'])
    def plot():
    
        query = "SELECT fruit_name, quantity FROM fruits"
        result = fetchFromDatabase(mydb, query)

        # Extract labels and values from the result
        labels = [res[0] for res in result]
        values = [res[1] for res in result]
        fig = go.Figure(data=go.Bar(x=labels, y=values))
        
        fig.update_layout(title='Fruit Quantity Chart', xaxis_title='Fruits', yaxis_title='Quantity')
        fig.show()
       
        plt.bar(labels, values)
        plt.xlabel('Fruits')
        plt.ylabel('Quantity')
        plt.title('Fruit Quantity Chart')

    
       
        # chart_image = io.BytesIO()
        # plt.savefig(chart_image, format='png')
        # chart_image.seek(0)
        # plt.clf()
        
        # chart_base64 = base64.b64encode(chart_image.getvalue()).decode('utf-8')

        #return render_template('plot.html')



 
    @app.route('/search',methods=['GET','POST'])
    def search():
        if request.method == 'POST':
            fruit_name = request.form['fruit_name']
            mycursor.execute(search_query,(fruit_name,))
            result = mycursor.fetchall()
            return render_template("search.html",data=result)
        return render_template("search.html")

    return app

if __name__ == "__main__":
    app = createApp()
    app.run()