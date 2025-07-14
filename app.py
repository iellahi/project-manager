
#NEED TO FIX ISSUE: USERNAME/PASSWORD INCORRECT, POSSIBLY SQL ISSUE

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required#, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Check if any field is empty
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Get form values
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("confirmation")

        # Make sure password is strong
        if len(password) < 6:
            return apology("password should be at least 6 characters")
        #Check if passwords match
        if password != repassword:
            return apology("passwords do not match")

        # Check if entered username is different from those in database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(user) != 0:
            return apology("username already exists")

        # Hash password
        hashed = generate_password_hash(password, method="pbkdf2:sha256", salt_length = 8)

        # Enter username and password into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def projects():
    """Show detailed list of projects"""
    if request.method == "POST":

        if request.form.get("add"):

            return render_template("editor.html")

        elif request.form.get("edit"):

            # Take project name, get information of project, display information in editor
            projects = db.execute("SELECT * FROM projects WHERE title = ?", request.form.get("title"))

            if not projects:
                return apology("Create a project first")


            return render_template("editor2.html", project=projects)

    else:

        # Display sql table
        current_user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

        projects = db.execute("SELECT * FROM projects WHERE creator_id = ? OR permission_1 = ? OR permission_2 = ? ORDER BY date DESC", session["user_id"], current_user[0]['username'], current_user[0]['username'])
        return render_template("projects.html", projects=projects)


@app.route("/history")
@login_required
def history():
    """Show list of deleted projects"""
    current_user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    completed_projects = db.execute("SELECT * FROM completed_projects WHERE creator_id = ? OR permission_1 = ? OR permission_2 = ? ORDER BY completion_date DESC", session["user_id"], current_user[0]['username'], current_user[0]['username'])
    deleted_projects = db.execute("SELECT * FROM deleted_projects WHERE creator_id = ? OR permission_1 = ? OR permission_2 = ? ORDER BY deletion_date DESC", session["user_id"], current_user[0]['username'], current_user[0]['username'])

    return render_template("history.html", completed_projects=completed_projects, deleted_projects=deleted_projects)



@app.route("/editor", methods=["GET", "POST"])
@login_required
def editor():
    """Edit projects"""
    if request.method == "POST":

        #Get form data
        title = request.form.get("title")
        summary = request.form.get("summary")
        todo_list = request.form.get("todo_list")
        permission_1 = request.form.get("permission_1")
        permission_2 = request.form.get("permission_2")
        creator_id = session["user_id"]

        project = db.execute("SELECT * FROM projects WHERE title = ?", title)

        if request.form.get("submit") or request.form.get("submit_2"):

            # If username in permissions does not exist
            if permission_1:
                if not db.execute("SELECT username FROM users WHERE username = ?", permission_1):
                    return apology("Invalid username in permissions")

            if permission_2:
                if not db.execute("SELECT username FROM users WHERE username = ?", permission_2):
                    return apology("Invalid username in permissions")

            # If project title already exists.  TODO.   .
            if len(project) != 0 and request.form.get("submit"):
                return apology("Invalid title")

            # If project already exists
            if request.form.get("submit_2"):
                # Edit data
                db.execute("UPDATE projects SET summary = ?, todo_list = ?, permission_1 = ?, permission_2 = ? WHERE title = ?", summary, todo_list, permission_1, permission_2, project[0]['title'])
            else:
                # Add data
                db.execute("INSERT INTO projects (title, summary, todo_list, permission_1, permission_2, creator_id) VALUES (?, ?, ?, ?, ?, ?)", title, summary, todo_list, permission_1, permission_2, creator_id)

            # Redirect to projects
            return redirect("/")

        elif request.form.get("complete"):
            # Add project to completed table
            db.execute("INSERT INTO completed_projects (id, title, summary, creation_date, creator_id, permission_1, permission_2) VALUES (?, ?, ?, ?, ?, ?, ?)", project[0]['id'], title, summary, project[0]['date'], session["user_id"], permission_1, permission_2)
            db.execute("DELETE FROM projects WHERE id = ?", project[0]['id'])

            return redirect("/")

        elif request.form.get("abandon"):
            # Delete project from completed table
            db.execute("INSERT INTO deleted_projects (id, title, summary, creation_date, creator_id, permission_1, permission_2) VALUES (?, ?, ?, ?, ?, ?, ?)", project[0]['id'], title, summary, project[0]['date'], session["user_id"], permission_1, permission_2)
            db.execute("DELETE FROM projects WHERE id = ?", project[0]['id'])

            return redirect("/")

    else:

        return render_template("editor.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")