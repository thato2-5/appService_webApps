# Required modulea for flask web app
from flask import Flask, render_template

# Create the app instance here 
app = Flask(__name__)

# default route
@app.route('/')
def index():
  return render_template('index.html')

# Run app instance here
if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.')
