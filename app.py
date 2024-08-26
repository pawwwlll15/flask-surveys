#dont forget to add session from Flask so that the list is only stored within each session, this will allow 2 people to fill out the same survey at the same time
#importing flash will allow us to use flash messaging depending on logic on our route pages
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
#this is defining which survey we are using from the surveys.py file
from surveys import satisfaction_survey as survey

#avoiding mis spelling in future
RESPONSES = 'responses'

#connect Flask with this application
app = Flask(__name__)
#configure a secret key for mulitple security issues
app.config['SECRET_KEY'] = 'bologna'
#prevent debugger tool from preventing redirects
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#connecting debug toolbar to this specific app
debug = DebugToolbarExtension(app)


@app.route('/')
def start_survery():
    """assign satisfaction_survey to survey to use in survey.html"""

    return render_template("survey_start.html", survey = survey)


@app.route('/begin',methods=["POST"])
def begin_survey():
    """recieves post request from survey_start.html and then clears the responses for this sessioin and redirect to the first question on the survey"""

    session[RESPONSES] = []
    
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def hande_questions():
    """receives post request from /questions/<int:qid> and stores that data in a list of responses from this session and redirect to the next question on the survey"""

    #get responses
    choice = request.form['answer']

    #add response to session and then append choice to responses
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    #if responses length is the same as questions length, we have completed the survey
    if(len(responses) == len(survey.questions)):

        return redirect('/complete')
    
    else:
        
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current questions"""
    responses = session[RESPONSES]

    if(responses is None):
         #trying to access question page to soon
        return redirect('/')
    
    if(len(responses) == len(survey.questions)):
        #if you have the same amount of responses as you do questions, which means you answered all questions and are finished.
        return redirect('/complete')
    
    if(len(responses) != qid):
        #flash a message if len of responses does not equal qid
        flash(f"Invalid question id: {qid}")

    question = survey.questions[qid]
    return render_template('question.html', question_num=qid, question = question)


@app.route('/complete')
def complete():
    """Survey complete, show complete page"""

    responses = session[RESPONSES]
    return render_template('completion.html', responses = responses)

