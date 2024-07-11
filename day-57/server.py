from flask import Flask, render_template
import random
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.today().year
    my_name = "Berkan Sözer"
    return render_template("index.html", num=random_number, current_year=current_year, my_name=my_name)

@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)

@app.route("/guess/<name>")
def guess(name):
    agify_result = requests.get(f"https://api.agify.io?name={name}")
    age_data = agify_result.json()
    age = age_data.get('age', 'unknown')
    return render_template("guess.html", name=name, age=age)

if __name__ == '__main__':
    app.run(debug=True)
