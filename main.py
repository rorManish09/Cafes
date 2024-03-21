from flask import Flask, render_template,url_for,redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,URLField , SelectField
from wtforms.validators import DataRequired , URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bafbsbufiwuibiqbdnzxnha'
Bootstrap5(app)


class CafeForm(FlaskForm):

    Coffee_items = ["☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️☕️","☕️☕️☕️☕️☕️️"]
    wifi_items = ["💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"]
    power_items = ["🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"]


    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = URLField('Location',validators=[DataRequired(),URL(require_tld=True)])
    open = StringField('Open',validators=[DataRequired()])
    close = StringField('Close',validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=Coffee_items)
    wifi = SelectField('Wifi', validators=[DataRequired()],choices=wifi_items)
    power = SelectField('Power', validators=[DataRequired()],choices=power_items)

    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi.data},"
                           f"{form.power.data}")
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
