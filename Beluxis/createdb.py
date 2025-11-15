from beluxis import app, db
from beluxis import models

def main() -> None:
    with app.app_context():
        db.create_all()
        print("Banco de dados criado/atualizado")

if __name__ == "__main__":
    main()

