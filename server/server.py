import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# instance relative config allows u to change dir path VIMP
server = Flask(__name__, instance_relative_config=True,template_folder='../client/')
server.static_folder = '../client/'
server.secret_key = "joe mama"
uploads_dir = os.path.join('client/')                                                                                                                                                                                                                

# filename = secure_filename("test_img.jpg")


@server.route('/')  # this decides if you need to run html or not
def init():
    return render_template('app.html')

#  try with png and others
@server.route("/", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(uploads_dir, filename))
            flash("Uploaded", 'upload')
            try:
                os.rename(uploads_dir+filename, uploads_dir + "test_img.jpg")
            except:
                pass
            return render_template('app.html',filename=filename)
    else:
        return redirect(request.url)

@server.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)

@server.route("/predict", methods=["POST","GET"])
def predict():
    if request.method == 'POST':
        try:
                import predict
                output=predict.predict()
                flash(output, 'predict')
                return redirect(url_for('predict'))
        except Exception as e:
                return str(e)
    else:
        return "Error! Please try again"


if __name__ == "__main__":
    server.run(debug=True)
