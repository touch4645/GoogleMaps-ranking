from flask import Flask, render_template, request
from src.modules.module import judge_key
import os
template_dir = os.path.abspath('src/templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/link')
def link():
    return render_template('link.html')


@app.route('/', methods=['GET', 'POST'])
def top():
    if request.method == 'GET':
        return render_template('top.html')
    if request.method == 'POST':
        url = request.form['url']
        context = judge_key(url)
        return render_template('result.html', context=context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)