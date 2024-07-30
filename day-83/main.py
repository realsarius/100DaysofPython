from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# def year_to_words(year):
#     num_to_words = {
#         20: 'twenty',
#         21: 'twenty-one',
#         22: 'twenty-two',
#         23: 'twenty-three',
#         24: 'twenty-four',
#     }
#     if year == 2024:
#         return 'twenty twenty-four'
#     elif year in num_to_words:
#         return num_to_words[year % 100]
#     else:
#         return str(year)

@app.route("/")
@app.route("/index")
def home():
    current_year = datetime.now().year
    # year_in_words = year_to_words(current_year)
    return render_template('index.html', current_year=current_year)

if __name__ == "__main__":
    app.run(debug=True)

