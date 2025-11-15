from beluxis import app, db
from beluxis.models import Cliente

with app.app_context():
    # Primeiro admin
    cliente1 = Cliente.query.filter_by(email='admin@example.com').first()
    if not cliente1:
        cliente1 = Cliente(usuario='admin', email='admin@example.com', is_admin=True)
        cliente1.set_password('admin123')
        db.session.add(cliente1)
        print('Admin criado: admin@example.com / admin123')
    else:
        print('Admin já existe: admin@example.com')

    # Segundo admin (adicione mais conforme necessário)
    cliente2 = Cliente.query.filter_by(email='admin2@example.com').first()
    if not cliente2:
        cliente2 = Cliente(usuario='admin2', email='admin2@example.com', is_admin=True)
        cliente2.set_password('admin456')
        db.session.add(cliente2)
        print('Admin criado: admin2@example.com / admin456')
    else:
        print('Admin já existe: admin2@example.com')

    db.session.commit()
