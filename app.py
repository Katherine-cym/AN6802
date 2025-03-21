from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os



app = Flask(__name__)

flag = 1
api = "AIzaSyCWPKr6v5uY_-BZvrOBQgrLB6JLNuZMTuU"
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key = api)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))


@app.route("/main",methods=["GET","POST"])
def main():
    global flag
    if flag == 1:
        t = datetime.datetime.now()
        user_name = request.form.get("q")   
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        conn.execute("INSERT INTO USER (name, timestamp) VALUES (?, ?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close() 
        flag = 0
    return(render_template("main.html"))


@app.route("/foodexp",methods=["GET","POST"])
def foodexp():   
    return(render_template("foodexp.html"))

@app.route("/ethical_test",methods=["GET","POST"])
def ethical_test():   
    return(render_template("ethical_test.html"))

@app.route("/FAQ",methods=["GET","POST"])
def FAQ():   
    return(render_template("FAQ.html"))

@app.route("/FAQ1",methods=["GET","POST"])
def FAQ1():   
    r = model.generate_content("Factors for Profit")

    return(render_template("FAQ1.html", r = r.candidates[0].content.parts[0].text))

@app.route("/userLog",methods=["GET","POST"])
def userLog():   
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM USER")
    r = ""
    for row in c:
        r = r+str(row) + "\n"
    print(r)
    c.close()
    conn.close()
    return(render_template("userLog.html",r=r))

@app.route("/deleteLog",methods=["GET","POST"])
def deleteLog():   
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("DELETE FROM USER")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("deleteLog.html"))

'''
@app.route("/test_result",methods=["GET","POST"])
def test_result():  
    answer = request.form.get("answer")
    if answer =="false": 
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))
'''
@app.route("/foodexp_pred",methods=["POST","GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html", r = (q*0.4851+ 147.475)))


@app.route("/test_result",methods=["POST","GET"])
def test_result():
    answer=request.form.get("answer")
    if answer=="false":
        return(render_template("pass.html"))
    elif answer=="true":
        return(render_template("fail.html"))

if __name__ == "__main__":
    app.run()