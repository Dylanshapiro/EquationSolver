import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, render_template, send_from_directory
from werkzeug.utils import secure_filename
from Solver.EquationSolver import CVES

UPLOAD_FOLDER = os.getcwd() + '\\uploads'
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

solver = CVES()

# Register itself as the main route
main = Blueprint('main', __name__)


'''
Check the file has allowed extension

! BE CAREFUL ! this is not a thorough check if you want to use
this in production you will need a more rigorous check. 
If you are interested in using this in production please connect me
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
Index page where a user can upload a file
'''
@main.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template("index.html")

'''
Show results of the equation processed
'''
@main.route('/solve', methods=['GET', 'POST'])
def solve():
    pageData = {}
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            equation, answer = solver.solve(path)
            pageData = {
                "Original": filename,
                "Boxed": filename[:-4] + "_boxed" + filename[-4:],
                "Equation": equation,
                "Answer": answer
            }
    return render_template("view.html", pageData=pageData)

'''
Get file, particular image
'''
@main.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)