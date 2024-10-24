from extensions import db

class UserSapiens(db.Model):
    __tablename__ = 'user_sapiens'
    
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(50), nullable=False, default='standard')
    apply = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"<UserSapiens {self.username}>"
