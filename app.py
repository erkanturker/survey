from flask import Flask,render_template,session,redirect,request,flash,make_response
from surveys import satisfaction_survey as survey
from surveys import surveys

RESPONSES_KEY = "responses"
CURRENT_SURVEY_KEY = 'current_survey'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'


@app.route("/")
def show_pick_survey_form():
    return render_template("pick-survey-form.html",surveys=surveys)

@app.route("/",methods=['POST'])
def pick_survey():
    surveyKey = request.form['survey']

    isCompleted =bool(request.cookies.get(f"is_{surveyKey}_Survey_Completed"))
    if isCompleted:
        flash("You already completed the survey")
        return redirect("/thanks")
    
    session[CURRENT_SURVEY_KEY]=surveyKey
    survey = surveys[surveyKey]

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):

    survey = surveys[session[CURRENT_SURVEY_KEY]]
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
    text = request.form.get('text',"")

    """add response to the session array"""
    responses = session[RESPONSES_KEY]
    responses.append({"choise":choise,"text":text})
    session[RESPONSES_KEY]= responses

    """if they answer the all the question redirect to thanks page"""
    if len(responses)==len(survey.questions):
        return redirect("/thanks")
    else: 
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def show_completion_page():
    surveyKey = session[CURRENT_SURVEY_KEY]
    survey= surveys[surveyKey]
    responses= session[RESPONSES_KEY]

    html = render_template("completion.html",survey=survey,responses=responses)

    response = make_response(html)

    response.set_cookie(f"is_{surveyKey}_Survey_Completed","True")

    return response





