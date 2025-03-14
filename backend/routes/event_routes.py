from flask import Blueprint, jsonify, request, make_response
from extensions import db
from models import Event

event_bp = Blueprint("event_bp", __name__)

@event_bp.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])
@event_bp.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "name" not in data or "date" not in data or "total_bill" not in data:
        return make_response(jsonify({"error": "Thiếu thông tin name, date hoặc total_bill"}), 400)

    new_event = Event(
        name=data["name"],
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        total_bill=data["total_bill"]
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201
@event_bp.route("/events/<int:id>", methods=["PUT"])
def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event không tồn tại"}), 404

    data = request.get_json()
    if "name" in data:
        event.name = data["name"]
    if "date" in data:
        event.date = datetime.strptime(data["date"], "%Y-%m-%d")
    if "total_bill" in data:
        event.total_bill = data["total_bill"]

    db.session.commit()
    return jsonify(event.to_dict()), 200
@event_bp.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event không tồn tại"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event đã bị xóa"}), 200
