from flask import Blueprint, jsonify, request, make_response
from extensions import db
from models.models import Events
from datetime import datetime

event_bp = Blueprint("event_bp", __name__)

#1.Xem thông tin toàn bộ sự kiện
@event_bp.route('/events', methods=['GET'])
def get_events():
    events = Events.query.all()  # Lấy tất cả dữ liệu từ bảng
    return jsonify([event.to_dict() for event in events])  # Trả về danh sách JSON

#2.Thêm sự kiện
@event_bp.route('/events', methods=["POST"])  
def post_events():
    data_list = request.get_json()
    # Kiểm tra xem data có phải là danh sách không
    if not isinstance(data_list, list):
        return jsonify({"error": "Input must be a list of events"}), 400
    added_events = []  # Danh sách lưu các sự kiện đã thêm
    skipped_events = []  # Danh sách lưu các sự kiện bị bỏ qua
    for data in data_list:
         # if data["name"] == None or data["date"] == None:
        if not data or 'name' not in data or 'date' not in data or not data["name"].strip() or not data["date"].strip():
            skipped_events.append({"data":data,
                                 "message_error":"something exist in not data or name not in data or date not in data or not data.name or not data.date"
                                 })
            continue
        try:
            event_date = datetime.strptime(data["date"], "%d-%m-%Y")
        except ValueError as ex:
            skipped_events.append({"data":data,
                                 "message_error":"date value error"
                                 })
            continue
        new_event = Events(
                name=data["name"],
                date=event_date,
                total_bill=data.get("total_bill", None)
            )
        db.session.add(new_event)
        added_events.append(new_event.to_dict())
    try:
        db.session.commit()
        return jsonify({"message": "cap nhat thanh cong",
                        "list_added-event": added_events,
                        "list_skipped-event": skipped_events
                        })
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": f"Lỗi khi cập nhật sự kiện: {str(ex)}"})

   
#3. lấy thông tin sự kiện cụ thể
@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event_id(event_id):
    events = Events.query.get(event_id)
    if not events:
        return jsonify({"error":"event not found"}),404
    return jsonify(events.to_dict())

#4. Xóa sự kiện
@event_bp.route('/events/<int:event_id>', methods=["DELETE"])
def delete_event_id(event_id):
    events = Events.query.get(event_id)
    if not events:
        return jsonify({"error":"event not found"}),404
    try:
        db.session.delete(events)
        db.session.commit()
        return jsonify("delete successfully")
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}),500
    
#5. Chỉnh sửa sự kiện
@event_bp.route('/events/<int:event_id>', methods = ["PUT"])
def adjust_event_id(event_id):
    events =Events.query.get(event_id)
    
    # kiểm tra xẽm sự kiện có tồn tại không
    if  not events:    
        return jsonify("error: khong cos su kien")
    data = request.get_json()
    
    # kiểm tra xem tên co rỗng không nếu nhập.
    if 'name' in data: 
        if not data['name']:
            return jsonify({"error": "ten khong dc de trong"})   
    # nhập ngày phải đúng mẫu '%Y-%m-%d %H:%M:%S'
    if 'date' in data:
        try:
            events.date = datetime.strptime(data['date'], "%d-%m-%Y")     
        except Exception as e:
            return "error: nhap thieu thong tin ngay tao"
    # Sửa sự kiện nếu có thì sửa không thì giữ nguyên.
    events.name = data.get('name',events.name)
    events.total_bill = data.get('total_bill',events.total_bill)
    
    try:
        db.session.commit()
        return jsonify({"da cap nhat thanh cong ":events.to_dict()})
    except Exception as ex:
        return jsonify(str(ex))
    