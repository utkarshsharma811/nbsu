import os

from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
from flask_mysqldb import MySQL
from flask_session import Session
from app import *
from passlib.hash import bcrypt
from datetime import date

main = Blueprint('main', __name__)

def execute_db(query,args=()):
    try:
        cur=mysql.connection.cursor()
        cur.execute(query,args)
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
    finally:
        cur.close()


@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@main.route("/stats/", methods=["POST", "GET"])
def stats():
    return render_template("stats.html")


@main.route("/patiala/", methods=["POST", "GET"])
def patiala():
    
    return render_template("patiala.html")


@main.route("/ludhiana/", methods=["POST", "GET"])
def ludhiana():

    return render_template("ludhiana.html")

@main.route("/amritsar/", methods=["POST", "GET"])
def amritsar():

    return render_template("amritsar.html")


@main.route("/login/", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        query  = query_db("select pass from hospital where id=%s",(username, ))
        if query is None:
            flash("Incorrect Credentials!", "danger")
            return redirect(url_for('main.login'))
        else:
            if password==query[0][0]:
            #if bcrypt.verify(password, query[0][0]):
                session["n_id"] = username
                flash("Login Successful", "success")
                return render_template("hospital_portal.html")

            else:
                flash("Incorrect Credentials", "danger")
                return redirect(url_for('main.login'))
    return render_template("login.html", **locals())

@main.route('/logout/', methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@main.route('/hospital_portal/', methods=["GET", "POST"])
@login_required
def hospital_portal():
    return render_template("hospital_portal.html")
    
@main.route('/add_patient/', methods=["GET", "POST"])
@login_required
def add_patient():
    if request.method=="POST":
        print(request.form)
        mrn = request.form["mrn"]
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        contact = request.form["contact"]
        adm_m = request.form["adm_m"]
        adm_y = request.form["adm_y"]
        bg = request.form["bg"]
        bp = request.form["bp"]
        diab = request.form["diab"]
        disease = request.form["disease"]
        descrip = request.form["descrip"]        

        queries = query_db("SELECT * FROM hospital where n_id = %s;", session["n_id"])
        for query in queries:
            dist= query[3];
        execute_db("INSERT INTO patient(mrn, name, age, gender, contact, email, adm_m, adm_y, bg, bp, diab, allergy, disease, descrip, dist) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (mrn, name, age, gender, contact, email, adm_m, adm_y, bg, bp, diab, allergy, disease, descrip, dist ))
        flash("Data Inserted Successfully!","success")
        return redirect(url_for('main.add_patient'))

    return render_template("add_patient.html")
 
@main.route('/view_patient/', methods=["GET", "POST"])
@login_required
def view_patient():
    
    mrn = request.form["MRN"]
    dis_m = request.form["dis_m"]
    dis_y = request.form["dis_y"]    

    if request.method=="POST":
        execute_db("UPDATE hospital SET dis_m = %s WHERE mrn = %s;", (dis_m, mrn))
        execute_db("UPDATE hospital SET dis_y = %s WHERE mrn = %s;", (dis_y, mrn))
        flash("Discharged Successfully!","success")
        return redirect(url_for('main.view_patient'))

    else:
        flash("Could not discharge!","danger")
        return redirect(url_for('main.view_patient'))

    return render_template("view_patient.html")
    