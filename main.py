from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditor, CKEditorField
import smtplib
import re
my_email = 'mah.talaat1087@gmail.com'
password ="thegreatwilbereat"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

class ContactMeForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Enter your email-address', validators=[DataRequired()])
    message = CKEditorField('your message', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['POST', 'GET'])
def home():
    form = ContactMeForm()
    re_html = re.compile(r'<[^>]+>')
    if form.validate_on_submit():
        message = re_html.sub('', request.form['message'])
        email = request.form['email']
        with smtplib.SMTP('smtp.gmail.com', port=587)as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f'the message is from {email} and its says: {message}')
            return redirect(url_for('home'))

    return render_template('index.html')


@app.route('/contact_me')
def contact():
    form = ContactMeForm()
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
