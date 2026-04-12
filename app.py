from flask import Flask, render_template, request, redirect
from miscellaneous.states import us_states
import random

app = Flask(__name__, static_folder='static', static_url_path= '/', template_folder='templates')

@app.route('/', methods=['GET','POST'])
def home():
    yourname = ''
    if request.method == 'POST':
        yourname = request.form.get('yourname')
    return render_template('home.html', message= yourname)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/state_abbreviation', methods=['GET','POST'])
def state_abbreviation():
    full_state_name = ''
    abbreviation = ''
    if request.method == 'POST':
        abbreviation = request.form.get('state_abbreviation')
        full_state_name = us_states[abbreviation]
    return render_template('state_abbreviation.html', us_states=us_states, full_state_name=full_state_name, abbreviation=abbreviation)

@app.route('/calculator',methods=['GET','POST'])
def calculator():
    result =''
    first_number = ''
    second_number = ''  
    operator = ''
    if request.method == 'POST':
        first_number = request.form.get("first_number")
        second_number = request.form.get("second_number")
        operator = request.form.get("operator")

        if operator == "+":
            result = float(first_number) + float(second_number)
        elif operator == "-":
            result = float(first_number) - float(second_number)
        elif operator == "X":
            result = float(first_number) * float(second_number)
        else:
            if float(second_number) == 0:
                result = "Error - Cannot divide by zero"
            else:
                result = float(first_number) / float(second_number)
       
    return render_template('calculator.html',result=result,first_number=first_number,second_number=second_number,operator=operator)

@app.route('/guess_number', methods=['GET','POST'])
def guess_number():
    level = ''
    attempts = '' 
    target = '' 
    result = '' 
    guess = '' 
    count = ''
    if request.method == 'POST':
        level = int(request.form.get('level'))
        attempts = int(request.form.get('attempts'))
        guess = int(request.form.get('guess', 0))
        count = int(request.form.get('count', 0))
        target = int(request.form.get('target',0))

        if not target:
            if level == 1:
                target = random.randint(1, 9)
            elif level == 2:
                target = random.randint(10, 99)
            else:
                target = random.randint(100, 999)

        if guess:
            if count < attempts:
                if guess == target:
                    result = "Congratulations! You guessed the number."
                else:                  
                    result = "Sorry, that's not the correct number. Try again."
                    count += 1
            if count >= attempts:
                result = f"Out of attempts - the number was {target}."

    return render_template('guess_number.html', level=level, result=result, attempts=attempts, guess=guess, count=count, target=target)

if __name__ == '__main__':
    app.run(debug=True)





