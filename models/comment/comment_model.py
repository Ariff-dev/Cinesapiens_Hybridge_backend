from extensions import db

class CommentPost(db.Model):
    __tablename__ = 'comment_post'
    
    id_comment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user_sapiens.id_user'), nullable=False)
    id_post_sa = db.Column(db.Integer, db.ForeignKey('post_sapiens.id_post_sa'), nullable=False)
    comment_user_post = db.Column(db.Text, nullable=False)
    
    # Relación con el modelo UserSapiens
    user = db.relationship('UserSapiens', backref='comments')
    
    # Relación con el modelo PostSapiens
    post = db.relationship('PostSapiens', backref='comments')
    
    def __repr__(self):
        return f"<CommentPost {self.id_comment} by User {self.id_user}>"
