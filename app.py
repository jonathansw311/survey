from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

import surveys


app = Flask(__name__)
app.config['SECRET_KEY']="fenway2023"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False


#questionNum=0



@app.route('/')
def home_page():
  
   return render_template('start.html')

@app.route('/init', methods=['POST'])
def init():
    global a
    global resp

    resp = request.form.get('survey')
    if resp == 'satisfaction_survey':
        a = surveys.satisfaction_survey
    else:
        a = surveys.personality_quiz
    
    if session.get('personalityCompleted', False) and a == surveys.personality_quiz:
        return redirect('/thankYouPC')
    
    if session.get('surveyCompleted', False) and a == surveys.satisfaction_survey:
        return redirect('/thankYouPC')
    
    session['responses'+resp]=[]
    
    return redirect('question/0')
   
    
@app.route('/question/<q>' )
def question(q):
    qInt = int(q)
    
    if qInt != len(session['responses'+resp]):
        flash(f"""Please answer the questions in order! You have been redirected to question {len(session['responses'])}!""")
        return redirect("/question/"+str(len(session['responses'+resp])))
    questionNo = qInt
    qInt += 1
    choices = a.questions[questionNo].choices
    nextPage="/answer/"+str(qInt)
   
    return render_template('question.html',  a = a, questionNo =questionNo, choices= choices, nextPage=nextPage ) 
        
@app.route('/answer/<q>', methods=["POST"])
def answer(q):
    answer = request.form["choice"]
    responses = session['responses'+resp]
    responses.append(answer)

    session['responses'+resp]= responses
    
    if len(a.questions) != len(responses):
        return redirect('/question/'+q)
    else:
        return redirect('/thankYou')




@app.route('/thankYou' )
def thankYou():
    
    if a == surveys.personality_quiz:
        session['personalityCompleted']=True
    else:
        session['surveyCompleted']=True
        
    print(session['responses'+resp])
   
    return render_template('thankYou.html', responses = session['responses'+resp], a=a)


@app.route('/thankYouPC')
def thankYouPC():
    asdf = 'surveys.'+resp+'.title'
    return render_template('thankYouPC.html', resp=resp)