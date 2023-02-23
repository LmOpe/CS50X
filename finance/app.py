import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]

    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", id)
    cash = db.execute("SELECT * FROM users WHERE id = ?", id)
    grand_total = db.execute("SELECT * FROM grand_total WHERE user_id = ?", id)

    return render_template("/index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        check = shares.isdecimal()
        id = session["user_id"]
        now = datetime.now()
        transacted = now.strftime("%d/%m/%Y %H:%M:%S")

        # Ensure user inputs symbol
        if not symbol:
            return apology("Please input Symbol", 401)

        # Ensure symbol is valid
        if not lookup(symbol):
            return apology("Invalid symbol!")

        # Ensure user inputs number of shares
        if not shares:
            return apology("Please input the number of shares")

        # Ensure user inputs invalid number of shares
        if shares is '0' or not check:
            return apology("Number of shares must be a positive integer!")

        # Get the stock's current price
        price = lookup(symbol).get("price")

        total = float(shares) * price

        # Get the user's current balance
        balance = db.execute("SELECT cash FROM users WHERE id = ?", id)

        # Get the first dictionary from the returned list of dictionaries 
        b = balance[0]
        b_values = list(b.values())[0]
        if total > float(b_values):
            return apology("Insufficient balance!!", 400)

        # Store information about user's purchase
        db.execute("INSERT INTO bought (user_id, symbol, name, shares, price, total, transacted) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   id, symbol, lookup(symbol).get("name"), int(shares), price, total, transacted)
        
        # Update users cash balance to reflect new purchase
        db.execute("UPDATE users SET cash = (SELECT cash - (SELECT total FROM bought WHERE user_id = ? AND shares = ? AND symbol = ?) FROM users WHERE id = ?) WHERE id = ?", id, shares, symbol, id, id)
                
        # Update users stocks
        check_symbol = db.execute("SELECT symbol FROM stocks WHERE user_id = ? AND symbol = ?", id, symbol)
        if not check_symbol:
            db.execute("INSERT INTO stocks (user_id, symbol, name, shares, price, total) VALUES(?, ?, ?, ?, ?, ?)",
                       id, symbol, lookup(symbol).get("name"), shares, price, total)
        else:
            db.execute("UPDATE stocks SET shares = (SELECT SUM(shares) FROM bought WHERE user_id = ? AND symbol = ?), total = (SELECT SUM(total) FROM bought WHERE user_id = ? AND symbol = ?) WHERE user_id = ? AND symbol = ?", id, symbol, id, symbol, id, symbol)
         
        # Update grand_total
        check_id = db.execute("SELECT user_id FROM grand_total WHERE user_id = ?", id)
        if not check_id:
            db.execute("INSERT INTO grand_total (user_id, total) VALUES(?, ?)", id, 10000)
        else:
            db.execute("UPDATE grand_total SET total = (SELECT cash + (SELECT SUM(total) FROM stocks WHERE user_id = ?) FROM users WHERE id = ?) WHERE user_id = ?", id, id, id)

        # redirect user to homepage
        return redirect("/")

    # if user reached via GET
    else:
        return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    # Get list of data from database
    histories = db.execute("SELECT symbol, shares, price, transacted FROM bought WHERE user_id = ?", id)

    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # User reached route via POST
    if request.method == "POST":

        symbol = request.form.get("symbol")

        # Ensure symbol is inputted
        if not symbol:
            return apology("Please input a symbol!", 400)
        
        # Ensure symbol is valid
        if not lookup(symbol):
            return apology("Invalid symbol", 400)
        
        # Redirect user to quoted
        return render_template("/quoted.html", quotes=lookup(symbol))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/quote.html")

    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check username in database
        name = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        password = request.form.get("password")

        # Ensure username is inputted
        if not request.form.get("username"):
            return apology("Please input a username", 400)
        
        # Check if username already exists
        elif name:
            return apology("Username already exists", 400)

        # Ensure password is inputted
        if not password:
            return apology("Please input a password", 400)
        
        # Ensure confirm password is inputted
        elif not request.form.get("confirmation"):
            return apology("Plese input the password again!", 400)
        
        # Ensures passwords match
        if password != request.form.get("confirmation"):
            return apology("passwords do not match!", 400)
        
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"),
                   generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        return redirect("/login")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 404)
        symbol = request.form.get("symbol").upper()
        sold_shares = request.form.get("shares")
        now = datetime.now()
        transacted = now.strftime("%d/%m/%Y %H:%M:%S")
        id = session["user_id"]

        shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?", id, symbol)
        
        check = sold_shares.isdecimal()
        values = list()
        for i in symbols:
            for value in i.values():
                values.append(value)

        if symbol not in values:
            return apology("Incorrect Symbol", 404)
            
        # Ensure user inputs number of shares
        if not sold_shares:
            return apology("Please input the number of shares")

        # Ensure user inputs invalid number of shares
        if sold_shares is '0' or not check:
            return apology("Number of shares must be a positive integer!") 

        # Get the first dictionary from the returned list of dictionaries 
        b = shares[0]
        b_values = list(b.values())[0]

        if int(sold_shares) > int(b_values):
            return apology("Number of shares exceeds the avalaible shares")
        
        # Use tuple to get price
        price = None
        for key, value in lookup(symbol).items():
            if key == "price":
                price = value
        total = float(sold_shares) * price

        # Store information about user's sales
        db.execute("INSERT INTO bought (user_id, symbol, name, shares, price, total, transacted) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   id, symbol, lookup(symbol).get("name"), ((-1) * int(sold_shares)), price, ((-1) * total), transacted)
        
        # Update users cash balance to reflect new sales
        db.execute("UPDATE users SET cash = (SELECT cash - (SELECT total FROM bought WHERE user_id = ? AND shares = ? AND symbol = ?) FROM users WHERE id = ?) WHERE id = ?",
                   id, ((-1) * int(sold_shares)), symbol, id, id)
                
        # Update users stocks
        db.execute("UPDATE stocks SET shares = (SELECT SUM(shares) FROM bought WHERE user_id = ? AND symbol = ?), total = (SELECT SUM(total) FROM bought WHERE user_id = ? AND symbol = ?) WHERE user_id = ? AND symbol = ?", id, symbol, id, symbol, id, symbol)
         
        # Update grand_total
        db.execute("UPDATE grand_total SET total = (SELECT cash + (SELECT SUM(total) FROM stocks WHERE user_id = ?) FROM users WHERE id = ?) WHERE user_id = ?", id, id, id)

        return redirect("/")
    else:
        return render_template("/sell.html", symbols=symbols)
