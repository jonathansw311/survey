from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

import surveys


app = Flask(__name__)
app.config['SECRET_KEY']="fenway2023"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

responses = []
questionNum=0
a= surveys.satisfaction_survey


@app.route('/')
def home_page():
  
   return render_template('start.html', a = a)
   
    
@app.route('/question/<q>' )
def question(q):
    global responses
    qInt = int(q)
    qsAnswered = len(responses)
    if qInt == 4:
        
        responses=[]
        return redirect('/question/0')
    if qInt != qsAnswered:
        flash(f"""Please answer the questions in order! You have been redirected to question {qsAnswered}!""")
        return redirect("/question/"+str(qsAnswered))
    questionNo = qInt
    qInt += 1
    choices = a.questions[questionNo].choices
    nextPage="/answer/"+str(qInt)
   
    return render_template('question.html',  a = a, questionNo =questionNo, choices= choices, nextPage=nextPage ) 
        
@app.route('/answer/<q>', methods=["POST"])
def answer(q):
    answer = request.form["choice"]
    responses.append(answer)
    
    if len(a.questions) != len(responses):
        return redirect('/question/'+q)
    else:
        return redirect('/thankYou')




@app.route('/thankYou' )
def thankYou():
    
    
    print(responses)
   
    return render_template('thankYou.html', responses = responses, a=a)