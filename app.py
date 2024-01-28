from flask import Flask,render_template,session,redirect,request,flash
from surveys import satisfaction_survey as survey
RESPONSES_KEY = "responses"


app = Flask(__name__)

app.config['SECRET_KEY'] = 'asd'

#toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):

    responses = session[RESPONSES_KEY]

    answerdQuestion = len(responses)
    surveyQuestion =len(survey.questions)

    if (answerdQuestion)<=0:
        qid=0
    elif answerdQuestion==surveyQuestion:
        return redirect("/thanks")
    elif qid!=answerdQuestion:
        qid=answerdQuestion
        flash(f"wrong question id Entered, you are rediceting question/{qid}")

    question = survey.questions[qid]
    return render_template("question.html",question=question)

@app.route("/answer",methods=["POST"])
def store_answer():
    """Save response and redirect to next question."""

    choise = request.form['answer']

    """add response to the session array"""
    responses = session[RESPONSES_KEY]
    responses.append(choise)
    session[RESPONSES_KEY]= responses

    """if they answer the all the question redirect to thanks page"""
    if len(responses)==len(survey.questions):
        return redirect("/thanks")
    else: 
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def show_completion_page():
    return render_template("completion.html")



