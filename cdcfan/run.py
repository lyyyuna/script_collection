from flask import Flask
import cdc

app = Flask(__name__)

@app.route('/cdc/')
def submit():
    cdc.submitcdcfan()
    return "haha"


if __name__ == '__main__':
    app.run()
