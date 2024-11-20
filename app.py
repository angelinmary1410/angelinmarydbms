from flask import Flask, render_template, request, redirect, url_for, flash

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'movie_booking'

# Helper function to connect to the database
def get_db_connection():
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return conn

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Movies')
    movies = cursor.fetchall()
    conn.close()
    return render_template('moviespage.html', movies=movies)

@app.route('/book/<int:movie_id>', methods=('GET', 'POST'))
def book(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Movies WHERE MovieID = %s', (movie_id,))
    movie = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        user_id = 1  # Example user ID, replace with actual user session logic
        seats = request.form['seats']
        booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert booking into Bookings table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Bookings (UserID, MovieID, BookingDate, Seats) VALUES (%s, %s, %s, %s)',
                       (user_id, movie_id, booking_date, seats))
        conn.commit()
        conn.close()
        flash('Booking successful!', 'success')
        return redirect(url_for('movies'))

    return render_template('bookingpage.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
