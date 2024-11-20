import pyodbc as pyo
from flask import Flask, request, jsonify, render_template
import logging
from datetime import datetime
import os


logger = logging.getLogger(__name__)
app = Flask(__name__)
app.json.sort_keys = False

# Connect to the database and return a dbc object
def get_db_connection():
    server = os.environ["SQL_server"]
    db = os.environ["SQLDB"]
    password = os.environ["SQL_PASS"]
    username = os.environ["SQL_USER"]
    cnn_azure = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={db};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    cnn = pyo.connect(cnn_azure)
    return cnn

#Init application by checks if table (restaurantTable and searchHistoryTable) exist and create it if its not
def app_init_db ():
    cnn = get_db_connection()
    cnn.execute(
        """
        if not exists (select * from sysobjects where name='restaurantTable' and xtype='U')
        CREATE TABLE [dbo].[restaurantTable](
        	[id] [int] IDENTITY(1,1) NOT NULL,
        	[restaurantName] [varchar](50) NOT NULL,
        	[restaurantStyle] [varchar](50) NULL,
        	[vegetarian] [bit] NULL,
        	[deliveries] [bit] NULL,
        	[timeOpen] [time](7) NULL,
        	[timeClose] [time](7) NULL,
         CONSTRAINT [PK_restaurantTable] PRIMARY KEY CLUSTERED 
        (
        	[id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]

        """
    )
    cnn.commit()
    cnn.execute(
        """
        if not exists (select * from sysobjects where name='searchHistoryTable' and xtype='U')
        CREATE TABLE [dbo].[searchHistoryTable](
	       [id] [int] IDENTITY(1,1) NOT NULL,
	       [searchTime] [time](7) NOT NULL,
	       [restaurantName] [varchar](50) NULL,
	       [restaurantStyle] [varchar](50) NULL,
	       [vegetarian] [varchar](50) NULL,
	       [deliveries] [varchar](50) NULL,
	       [searchMethod] [varchar](50) NOT NULL,
         CONSTRAINT [PK_searchHistoryTable] PRIMARY KEY CLUSTERED 
         (
	       [id] ASC
         )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
         ) ON [PRIMARY]
        """
    )
    cnn.commit()
    cnn.close()
app_init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Check database connection
@app.route('/db_connection', methods=['GET'])
def check_db_connection ():
    try:
        cnn = get_db_connection()
        cnn.close()
        return jsonify ({"message": "Database connection successful"}), 200
    except Exception as e:
        logger.error("Failed to connect error msg: %s",repr(e))
        return jsonify({"message": f"Database connection failed: {str(e)}"}), 500
 

# A decorator for password protection
def require_password(f):
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == app_user and auth.password == app_pass):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function



# Add restaurant by post request protected by user and password 
#curl -u admin:securepassword -X POST -H "Content-Type: application/json" -d '{"restaurantName": "Hummus Sababa"}' http://restaurant-app.com/add_restaurant
@app.route('/add_restaurant', methods=['POST'])
@require_password
def add_restaurant():
    restaurant_name = request.args.get('restaurantName')
    restaurant_style = request.args.get('restaurantStyle')
    vegetarian = request.args.get('vegetarian')
    deliveries = request.args.get('deliveries')
    time_open = request.args.get('timeOpen')
    time_close = request.args.get('timeClose')
    if not (restaurant_name and restaurant_style and vegetarian is not None and deliveries is not None and time_open and time_close):
        return jsonify({"message": "Missing mandatory parameters"}), 400
    try:
        conn = get_db_connection()
        conn.execute (""" 
                      INSERT INTO restaurantTable(restaurantName,restaurantStyle,vegetarian,deliveries,timeOpen,timeClose)
                      VALUES ('"""+restaurant_name+"""','"""+restaurant_style+"""','"""+vegetarian+"""','"""+deliveries+"""','"""+time_open+"""','"""+time_close+"""');    
                      """)
        conn.commit()
        conn.close()    
        return jsonify({"message": "Record added successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Failed to insert: {str(e)}"}), 500


# Search for restaurants that is open now with optional parameters eg /search?restaurantStyle=italian?vegetarian=true
@app.route('/search', methods=['GET'])
def search():
    restaurant_name = request.args.get('restaurantName')
    restaurant_style = request.args.get('restaurantStyle')
    vegetarian = request.args.get('vegetarian')
    deliveries = request.args.get('deliveries')

    query = "SELECT * FROM restaurantTable WHERE CONVERT(TIME, GETDATE()) BETWEEN timeOpen AND timeClose"
    params = []

    if restaurant_name:
        query += " AND restaurantName = ?"
        params.append(restaurant_name)
    else:
        restaurant_name = ""
    
    if restaurant_style:
        query += " AND restaurantStyle = ?"
        params.append(restaurant_style)
    else:
        restaurant_style = ""
    if vegetarian:
        query += " AND vegetarian = ?"
        params.append(vegetarian)
    else:
        vegetarian = ""
    if deliveries:
        query += " AND deliveries = ?"
        params.append(deliveries)
    else:
        deliveries = ""


    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        results = [
            {
                "restaurantName": row.restaurantName,
                "restaurantStyle": row.restaurantStyle,
                "vegetarian": row.vegetarian,
                "deliveries": row.deliveries,
                "timeOpen": str(row.timeOpen),
                "timeClose": str(row.timeClose)
            } for row in records
        ]
        now = datetime.now().strftime("%H:%M:%S")
        conn.execute (""" 
                      INSERT INTO searchHistoryTable(searchTime,restaurantName,restaurantStyle,vegetarian,deliveries,searchMethod)
                      VALUES ('"""+str(now)+"""','"""+restaurant_name+"""','"""+restaurant_style+"""','"""+vegetarian+"""','"""+deliveries+"""','search');    
                      """)
        conn.commit()
        conn.close()
        
        return jsonify(results), 200
    except Exception as e:
      return jsonify({"message": f"Failed to retrieve records: {str(e)}"}), 500

#Search by restaurantName /searchByRest?restaurantName=pizza
@app.route('/searchByRest', methods=['GET'])
def searchsimple():
 restaurant_name = request.args.get('restaurantName', type=str)
 query = "SELECT * FROM restaurantTable WHERE restaurantName = ?"
 params = [restaurant_name]
 try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        results = [
            {
                "restaurantName": row.restaurantName,
                "restaurantStyle": row.restaurantStyle,
                "vegetarian": row.vegetarian,
                "deliveries": row.deliveries,
                "timeOpen": str(row.timeOpen)[:-3],
                "timeClose": str(row.timeClose)[:-3]

            }for row in records]
        
        conn.close()
        return jsonify(results), 200
 except Exception as e:
      return jsonify({"message": f"Failed to retrieve records: {str(e)}"}), 500 

app_user = os.environ["APP_USER"]
app_pass = os.environ["APP_PASS"]

if __name__ == '__main__':
    app.run(host='0.0.0.0')