import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# instance relative config allows u to change dir path VIMP
app = Flask(__name__, instance_relative_config=True)
app.secret_key = "joe mama"
uploads_dir = os.path.join('static/')                                                                                                                                                                                                                

# filename = secure_filename("test_img.jpg")

@app.route('/')  # this decides if you need to run html or not
def init():
    return render_template('app.html')

#  try with png and others
@app.route("/", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(uploads_dir, filename))
            flash("Uploaded", 'upload')
            try:
                os.rename(uploads_dir+filename, uploads_dir + "test_img.jpg")
            except Exception as e1:
                print(e1)
            return render_template('app.html', filename="test_img.jpg")
    else:
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename="test_img.jpg"), code=301)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        import predict
        output = predict.predict()
        flash(str(output), 'predict')
        # return redirect(url_for('predict')) #bad
        return render_template('app.html', filename="test_img.jpg")  # good
        # return redirect(request.url) #bad
        # return redirect(request.referrer)  #bad
    except Exception as e2:
        print(e2)
        return str(e2)


if __name__ == "__main__":
    app.run(debug=True)
