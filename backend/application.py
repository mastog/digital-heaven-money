
from backend.models import models
from backend import routes, app, db

with app.app_context():
    db.create_all()
app.run(debug=True)