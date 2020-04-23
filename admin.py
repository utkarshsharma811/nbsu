from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
from app import *
from passlib.hash import bcrypt

admin = Blueprint('admin', __name__,url_prefix='admin')

@admin.route('/alogin/', methods=["GET", "POST"])
def login():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        query  = query_db("select password from admin where id=%s",(username, ))
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

    return render_template("admin_portal.html", **locals())


@admin.route('/logout/', methods=["GET", "POST"])
@admin_required
def logout():
    session.clear()
    return redirect(url_for("admin.login"))



@admin.route('/add_hospital/', methods=["GET", "POST"])
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
        return redirect(url_for('admin.login'))

    else:
        flash("Data not Inserted!","danger")
        return redirect(url_for('admin.login'))

    return render_template("add_hospital.html")

