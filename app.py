from flask import Flask, render_template, request, url_for, session, make_response
from miscellaneous.states import us_states
import random
import pandas as pd

app = Flask(__name__, static_folder='static', static_url_path= '/', template_folder='templates')
app.secret_key = '1st application development'

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

@app.route('/excel_upload', methods=['GET', 'POST'])
def excel_upload():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)
        return df.to_html()
    return render_template('excel_upload.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/temp_converter', methods=['GET','POST'])
def temp_converter():
    result_temp = ''
    original_temp = ''
    from_scale = ''
    to_scale = ''
    if request.method == 'POST':
        original_temp = float(request.form.get('original_temp'))
        from_scale = request.form.get('from_scale')
        to_scale = request.form.get('to_scale')
        
        if from_scale == to_scale:
            result_temp = original_temp
        elif from_scale == 'celsius':
            if to_scale == 'fahrenheit':
                result_temp = original_temp * 9 / 5 + 32
            elif to_scale == 'kelvin':
                result_temp = original_temp + 273.15
        elif from_scale == 'fahrenheit':
            if to_scale == 'celsius':
                result_temp = (original_temp - 32) * 5 / 9
            elif to_scale == 'kelvin':
                result_temp = (original_temp - 32) * 5 / 9 + 273.15
        elif from_scale == 'kelvin':
            if to_scale == 'celsius':
                result_temp = original_temp - 273.15
            elif to_scale == 'fahrenheit':
                result_temp = (original_temp - 273.15) * 9 / 5 + 32
    return render_template('temp_converter.html',result_temp=result_temp,original_temp=original_temp, from_scale=from_scale, to_scale=to_scale)

@app.route('/both_session_cookie', methods=['GET', 'POST'])
def session_cookie():
    message = ''
    message2 = ''
    if request.method == 'POST':
        set_session = request.form.get('set_session')
        get_session = request.form.get('get_session')
        clear_session = request.form.get('clear_session')
        set_cookie = request.form.get('set_cookie')
        get_cookie = request.form.get('get_cookie')
        clear_cookie = request.form.get('clear_cookie')

        if set_session:
            session['name1'] = 'Quang'
            session['pet1'] = 'chico'
            message = 'Session data set'
        elif get_session:
            if 'name1' in session.keys() and 'pet1' in session.keys():
                value1 = session['name1']
                value2 = session['pet1']
                message = f"[name1 : {value1}] , [pet1 : {value2}]"
            else:
                message = 'No session data found'
        elif clear_session:
            session.clear()
            message = 'Session cleared'
        elif set_cookie:
            response = make_response(render_template('session_cookie.html', message2 = 'Cookie set'))
            response.set_cookie(key='luno', value='augusta')
            return response
        elif get_cookie:
            if 'luno' in request.cookies:
                cookie_value = request.cookies['luno']
                message2 = f"Cookie value: {cookie_value}"
            else:
                message2 = 'No cookie found'
        elif clear_cookie:
            response = make_response(render_template('session_cookie.html', message2 = 'Cookie cleared'))
            response.set_cookie(key='luno', expires=0)
            return response

    return render_template('session_cookie.html', message=message, message2=message2)

def set_cookie():
    response = make_response(render_template('home.html', message = 'Cookie set'))
    response.set_cookie(key='cookie key', value='cookie value')
    return response

@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies['cookie key']
    return render_template('home.html', message = f"Cookie value: {cookie_value}")

@app.route('/clear_cookie')
def clear_cookie():
    response = make_response(render_template('home.html', message = 'Cookie cleared'))
    response.set_cookie(key='cookie key', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)





