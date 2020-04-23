from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
from app import *
from passlib.hash import bcrypt

admin = Blueprint('admin', __name__,url_prefix='/admin')

@admin.route('/login/', methods=["GET", "POST"])
def login():
    return render_template("admin_login.html", **locals())


@admin.route('/logout/', methods=["GET", "POST"])
@admin_required
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin.route('/login/portal/', methods=["GET", "POST"])
@admin_required
def portal():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        query  = query_db("select pass from admin where id=%s",(username, ))
        if query is None:
            flash("Incorrect Credentials!", "danger")
            return redirect(url_for('admin.login'))
        else:
            if bcrypt.verify(password, query[1]):
                session["admin_id"] = username
                flash("Login Successful", "success")
                return render_template("admin_portal.html")

            else:
                flash("Incorrect Credentials", "danger")
                return redirect(url_for('admin.login'))

@admin.route('/login/portal/add/', methods=["GET", "POST"])
@admin_required
def add_view():
    return render_template("add_nbsu.html")


@admin.route('/login/portal/add/submit/', methods=["GET", "POST"])
@admin_required
def add():
    if request.method=="POST":
        n_id = request.form["NBSU_ID"]
        name = request.form["NBSU_NAME"]
        password1 = request.form["pass"]
        address = request.form["NBU_ADDRESS"]
        dist = request.form["District"]
        mob = request.form["MOBILE"]
        password = bcrypt.using(rounds=8).hash(password1)

        execute_db("INSERT INTO t_nbsu VALUES (%s, %s, %s, %s, %s);", (n_id, name, address, dist, mob, password ))
        flash("Data Inserted Successfully!","success")
        return redirect(url_for('admin.portal'))

    else:
        flash("Data not Inserted!","danger")
        return redirect(url_for('admin.portal'))

@admin.route('/login/portal/delete/', methods=["GET", "POST"])
@admin_required
def delete_view():
    return render_template("delete_nbsu.html")

@admin.route('/login/portal/delete/submit/', methods=["GET", "POST"])
@admin_required
def delete():
    mrn = request.form["MRN"]
    con = request.form["confirm"]

    if con ==  "yes":

        if request.method=="POST":
            execute_db("UPDATE t_nbsu DELETE *  WHERE mrn = %s", (mrn))
            flash("NBSU deleted successfully", "success")
            return redirect(url_for('admin.delete_view'))
        else:
            flash("Could not delete NBSU!","danger")
            return redirect(url_for('main.dis_view'))
    else:
        flash("Could not delete NBSU!","danger")
        return redirect(url_for('main.dis_view'))
