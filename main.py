from flask import Flask, render_template, request, url_for, flash, redirect, session

import logging 

logging.basicConfig(level=logging.DEBUG)

# name of current python module
# used to tell the instance where it is located
app = Flask(__name__)

# USE SO I CAN STORE A TEMP DB?
app.secret_key = 'your_secret_key'  # random string (generate?)

# decorator
# render_template() utilizes Jinja template engine
# we can either use decorator or app.add_url_rule('/','hello',function)
@app.route('/', methods=('GET', 'POST'))
def index():
    app.logger.info('> Index page called')
    # init
    # Initialize URL_lst in the session

    app.logger.info(f'> SESSION BEFORE CHECK: {session["URL_lst"]}!')

    if 'URL_lst' not in session:
        session['URL_lst'] = []

    app.logger.info(f'> SESSION AFTER CHECK: {session["URL_lst"]}!')

    URL_lst = session['URL_lst']
    return render_template('index.html', URL_lst=URL_lst) 


@app.route('/add', methods=('GET', 'POST'))
def add():
    app.logger.info('> Add page called')
    if 'URL' in request.form:
        URL = request.form['URL'].strip()

        app.logger.info(f'> URL: {URL}')

        # if exists and not in session, add to session list
        if URL and URL not in session['URL_lst']:
            session['URL_lst'].append(URL)
            session.modified = True

            app.logger.info(f'> UNIQUE URL!')
            app.logger.info(f'> SESSION AFTER ADD: {session["URL_lst"]}!')
            
    return redirect('/')

@app.route('/delete', methods=('GET', 'POST'))
def delete():
    app.logger.info('Delete page called')
    i = int(request.form['INDEX'])
    
    session['URL_lst'].pop(i)
    session.modified = True

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)