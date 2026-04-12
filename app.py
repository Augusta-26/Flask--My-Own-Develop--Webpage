from flask import Flask, render_template, request, redirect

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

@app.route('/state_abbreviation')
def state_abbreviation():
    return render_template('state_abbreviation.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')



if __name__ == '__main__':
    app.run(debug=True)





