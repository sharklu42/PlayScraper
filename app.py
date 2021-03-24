from flask import Flask, render_template, request, send_file, after_this_request, current_app
import main
import os

app = Flask(__name__)

#rendering deafoult flask template
@app.route('/')
def index():
    return render_template("index.html")

#getting data from the input fields
@app.route('/get-data', methods=['POST'])
def my_form_post():
    keyword = request.form['keyword']
    country = request.form['country']
    locale = request.form['locale']
    app_id = request.form['app_id']
    main.run_script({"keyword": keyword, "country": country, "locale": locale, "app_id": app_id})
    file_path = "./output.csv"
#saving file into a memory to remove after downloding. Workaround for windows only
    def generate():
        with open(file_path) as f:
            yield from f

        os.remove(file_path)

    r = current_app.response_class(generate(), mimetype='text/csv')
    r.headers.set('Content-Disposition', 'attachment', filename='output.csv')
    return r


def get_index():
    return render_template()
