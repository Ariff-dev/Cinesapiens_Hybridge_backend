
from extensions import db

class PostSapiens(db.Model):
    __tablename__ = 'post_sapiens'
    
    id_post_sa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_name = db.Column(db.String(50), nullable=False)
    post_description = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<PostSapiens {self.post_name}>"
