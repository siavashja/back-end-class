import os

SECRET_KEY = "VoFEzeDFzXkMxMEFPpHPcpGV-vKqZcx8DafcVMh-EfA"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
ALGORITHM = "HS256"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
UPLOAD_FOLDER = UPLOAD_FOLDER.replace("\\",'/')