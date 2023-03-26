import os
import shlex
import subprocess

from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_mail import Attachment, Mail, Message
from markupsafe import escape
from werkzeug.utils import secure_filename

from .book import Book

load_dotenv()

ALLOWED_EXTENSIONS = {"epub", "mobi", "pdf", "txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
app.config["OUTPUT_FOLDER"] = os.getenv("OUTPUT_FOLDER")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["KINDLE_EMAIL"] = os.getenv("KINDLE_EMAIL")
mail = Mail(app)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return redirect("/upload")


@app.route("/success")
def upload_success():
    return "<h2>File successfully uploaded!</h2>"


# @app.route("/list-files")
# def get_files():
#     files = os.listdir(UPLOAD_FOLDER)
#     page_list = f""

@app.route("/upload", methods=["GET", "POST"])
def upload():
    # url_for("static", filename="style.css")

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            print(str(filename))
            # return redirect(url_for("download_file", name=filename))
            # TODO get title and author from filename"
            book = Book(str(filename))
            output_file_path = os.path.join(
                app.config["OUTPUT_FOLDER"], book.change_extension("epub"))
            print(output_file_path)
            # title = book.get_title()
            # author = book.get_author()
            # print(f"""
            #     Title: {title}
            #     Author: {author}""")
            # TODO run calibre script
            subprocess.call(
                shlex.split(
                    f'ebook-convert {filepath} {output_file_path} --smarten-punctuation'))
            # TODO change name of file and set details
            # TODO make loading screen/bar
            # TODO email file to kindle
            # book_atch = Attachment(
            # filename=f'{book.strip_extension()}', content_type='application/epub+zip', data=output_file_path)
            # msg = Message(subject=f'{book.strip_extension()}', sender='noreply@demo.com', recipients=[
            #               'cardoza.nick21@gmail.com'],
            #               attachments=[book_atch])
            msg = Message(subject='question', body="hello", sender='noreply@demo.com',
                          recipients=[app.config["KINDLE_EMAIL"]])
            # msg.body("This is a test email.")
            with app.open_resource(output_file_path) as fp:
                msg.attach(book.change_extension('epub'),
                           'application/epub+zip', fp.read())
            mail.send(msg)
            return "Email has been sent."
            # TODO make available for download but dont do so automatically
            return redirect(url_for('download'))

    return render_template('upload.html')


@app.route("/download")
def download():
    return render_template("download.html", files=os.listdir(app.config["OUTPUT_FOLDER"]))


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

# TODO dockerize


# app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
if __name__ == "__main__":
    app.run(debug=True)
