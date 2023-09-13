from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO
import bcrypt
import casagpio

# Algunas configuraciones para flask
app = Flask(__name__)
app.static_folder = 'static'  # Set the path to your static folder
app.static_url_path = '/static'  # Set the URL path for serving static files
app.secret_key = "embebidos2023"
app.debug = True

# Habilitar los CORS de la app para que funciones
CORS(app)
socketio = SocketIO(app)

# Hardcoded username and hashed_password for demonstration purposes
valid_username = 'asd123'
valid_password = 'asd123'
salt = bcrypt.gensalt()
hashed_valid_password = bcrypt.hashpw(valid_password.encode('utf-8'), salt)

# Se ponen los pines en los que se encuentra cada LED
pines = [
  {
    'target': 'LivingLightBulb',
    'pin': 0,
  },
  {
    'target': 'KitchenLightBulb',
    'pin': 1,
  },
  {
    'target': 'Bedroom1LigthBulb',
    'pin': 2,
  },
  {
    'target': 'Bedroom2LigthBulb',
    'pin': 3,
  },
  {
    'target': 'BathLigthBulb',
    'pin': 4,
  },
]

@app.route('/')
def index():
  if 'username' in session:
    return render_template('index.html')
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    if hashed_valid_password == hashed_password:
      session['username'] = username
      return redirect(url_for('index'))
    else:
      return "Invalid login credentials. Please try again."

  return render_template('login.html')

@socketio.on('connect')
def handle_connect():
  None

@socketio.on('SingleLED')
def handle_message(target, state):
  state = int(state)
  for pin in pines:
    if(pin['target'] == target):
      write_pin(pin['pin'], state)
  

@socketio.on('MultiLED')
def handle_message(state):
  state = int(state)
  for pin in pines:
    write_pin(pin['pin'], state)

@socketio.on('StateDOORS')
def handle_message():
  MainDoorSignal = bool(read_pin())
  Bedroom1DoorSignal = bool(read_pin())
  Bedroom2DoorSignal = bool(read_pin())
  BathDoorSignal = bool(read_pin())

  doors = [
    {
      'target': 'MainDoor',
      'value': MainDoorSignal,
    },
    {
      'target': 'Bedroom1Door',
      'value': Bedroom1DoorSignal,
    },
    {
      'target': 'Bedroom2Door',
      'value': Bedroom2DoorSignal,
    },
    {
      'target': 'BathDoor',
      'value': BathDoorSignal,
    },
  ]
  socketio.emit('StateDOORS', doors)

if __name__ == '__main__':
  init_gpio()
  socketio.run(app, host='localhost', port=5000)  # Replace with your desired host and port
