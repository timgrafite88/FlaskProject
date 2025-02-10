from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Настройки подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/ads_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель объявления
class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.String(100), nullable=False)

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

# Создание объявления
@app.route('/ads', methods=['POST'])
def create_ad():
    data = request.json
    ad = Ad(
        title=data['title'],
        description=data['description'],
        owner=data['owner']
    )
    db.session.add(ad)
    db.session.commit()
    return jsonify({'id': ad.id, 'title': ad.title, 'description': ad.description, 'owner': ad.owner, 'created_at': ad.created_at}), 201

# Получение всех объявлений
@app.route('/ads', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    return jsonify([{'id': ad.id, 'title': ad.title, 'description': ad.description, 'owner': ad.owner, 'created_at': ad.created_at} for ad in ads]), 200

# Удаление объявления
@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = Ad.query.get(ad_id)
    if not ad:
        return jsonify({'message': 'Ad not found'}), 404
    db.session.delete(ad)
    db.session.commit()
    return jsonify({'message': 'Ad deleted successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)