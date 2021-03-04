from app import app
from flask import render_template,url_for,redirect,request,abort,flash
from app.form import input_form
from app.match_word import Dictionary
import json
import pyttsx3

@app.route('/',methods=['GET'])
def dictionary(): 
    form = input_form()
    return render_template("index.html",form=form)



@app.route('/match',methods=['POST'])
def match():
    form = input_form()
    meaning = form.word.data
    dictionary = Dictionary(r'data.json') 
    
    if form.validate_on_submit():
    	#user input with capital letter
        if dictionary.find_key(form.word.data) == form.word.data.lower():
            output = dictionary.match(dictionary.find_key(form.word.data))
            return render_template("index.html",form=form,output=output,meaning=meaning)

    	#user input without capitalize
        elif dictionary.find_key(form.word.data) == form.word.data.capitalize():
            output = dictionary.match(dictionary.find_key(form.word.data))
            reminder = form.word.data.capitalize()+' :Name should be capitalized' 
            return render_template("index.html",form=form,output=output,meaning=meaning,reminder=reminder)
    	
        else:
            try:
                test = dictionary.close_match(form.word.data)[0]
                test_2 = dictionary.match(test)
                return redirect(url_for('error',form=form.word.data))

            except:
                error = 'This is not an English word. Please try again!'
                return render_template("index.html",form=form,error=error)

## Test for submission on error page
@app.route("/add",methods=["POST","GET"])
def add():
    if request.method == "POST":
        name = request.form.get("word")
        description = request.form.get("description")
        with open("data.json", "r+") as json_file:
            data = json.load(json_file)
            data[name] = [str(description)]
            json_file.seek(0)
            json.dump(data, json_file)
            json_file.truncate()
            flash(name + " has been added successfully😋", "success")
        return redirect(url_for("dictionary"))
    else:
        return render_template("error.html")

@app.route("/error")
def error():
    form = input_form()
    word = request.args.get('form')
    return render_template("error.html", form = form, word = word)









