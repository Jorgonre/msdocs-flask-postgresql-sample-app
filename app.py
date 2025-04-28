import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# Configuración
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI', 'sqlite:///restaurants.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Inicialización de la base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Los modelos deben ser importados después de la inicialización de la base de datos
from models import Restaurant, Review, ImageUpload

# Rutas existentes...
@app.route('/', methods=['GET'])
def index():
    print('Request for index page received')
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)

@app.route('/<int:id>', methods=['GET'])
def details(id):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    reviews = Review.query.where(Review.restaurant == id)
    return render_template('details.html', restaurant=restaurant, reviews=reviews)

@app.route('/create', methods=['GET'])
def create_restaurant():
    print('Request for add restaurant page received')
    return render_template('create_restaurant.html')

# Nueva ruta para subir imágenes
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Verificar si hay un archivo en la solicitud
        if 'image_file' not in request.files:
            return "No file part", 400
        file = request.files['image_file']

        # Si no seleccionaron un archivo
        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            # Asegurarse de que el nombre del archivo es seguro
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Guardar la imagen en el servidor
            file.save(filepath)

            # Obtener la hora de la subida
            upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Registrar la subida de la imagen en la base de datos (si deseas hacerlo)
            image_record = ImageUpload(image_path=filepath, upload_time=upload_time)
            db.session.add(image_record)
            db.session.commit()

            return f"Image uploaded successfully! Uploaded at: {upload_time}"

    return render_template('upload_image.html')  # Página con el formulario de carga de imágenes

# Método para verificar que el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Modelo de base de datos para almacenar la información de la imagen subida
class ImageUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    upload_time = db.Column(db.String(50), nullable=False)

# Rutas adicionales y utilidades...

if __name__ == '__main__':
    app.run()
