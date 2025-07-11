from flask import Flask, render_template, redirect
import subprocess
import os
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start_full")
def start_full():
    maincode_path = os.path.abspath("Maincode.py")
    print(f">> Maincode başlatılıyor: {maincode_path}")
    subprocess.Popen([sys.executable, maincode_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return redirect("/")

@app.route("/start_code")
def start_code():
    python_exe = sys.executable
    subprocess.Popen([python_exe, "code.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
