from .. import db

class categorysong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    musicType = db.Column(db.String(50), nullable=False)
    songs = db.relationship('Songs', backref='category', lazy=True)


class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songWriter = db.Column(db.String(100), nullable=False)
    songName = db.Column(db.String(120), nullable=False)
    songDescription = db.Column(db.Text, nullable=True)
    songDuration = db.Column(db.Text, nullable=True)
    songLink = db.Column(db.String(250), nullable=False)
    songCategory = db.Column(db.Integer, db.ForeignKey('categorysong.id'), nullable=True)
    songYear = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.songWriter}')"