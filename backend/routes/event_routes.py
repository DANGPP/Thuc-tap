from flask import Blueprint, jsonify, request, make_response
from extensions import db
from models.models import Events,Event_User,Users
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

#6. Thêm người vào 1 sự kiện
@event_bp.route("/events/<int:event_id>/users", methods=["POST"])
def post_user_to_event(event_id):
    event_check = Events.query.get(event_id)
    if not event_check:
        return jsonify({
            "error":"không tìm thấy event" 
        }),404
    data_user_list = request.get_json()

    # Kiểm tra xem data có phải là danh sách không
    if not isinstance(data_user_list, list):
        return jsonify({"error": "Không phải là List user"}), 400

    added_users = []
    not_added_users = []

    for user in data_user_list:
        user_id = user.get("user_id")
        bonusthem = user.get("bonusthem", "0")  
        # Kiểm tra user có tồn tại không
        User = Users.query.get(user_id)
        if not User:
            not_added_users.append({
                "user_id": user_id,
                "error": "Người dùng không tồn tại"
            })
            continue

        # Kiểm tra xem user đã có trong event chưa
        existing_entry = Event_User.query.filter_by(event_id=event_id, user_id=user_id)
        if existing_entry:
            not_added_users.append({
                "user_id": user_id,
                "error": "Người dùng đã tham gia sự kiện"
            })
            continue

        # Thêm user vào event
        new_event_user = Event_User(
            event_id=event_id,
            user_id=User.id,
            bonusthem=bonusthem,
            bill_due=0,
            status="Paid"
        )
        db.session.add(new_event_user)
        
        added_users.append({
            "user_id": User.id,
            "event_id": event_id
        })

    try:
        db.session.commit()
        return jsonify({
            "added_users": added_users,
            "not_added_users": not_added_users
        }), 201
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 500
    

#7. Lấy danh sách users từ sự kiện
@event_bp.route("/events/<int:event_idd>/users", methods=["GET"])
def get_users_in_event(event_idd):
    # Kiểm tra xem sự kiện có tồn tại không
    event = Events.query.get(event_idd)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Lấy sự kiện theo event_id
    event_users = Event_User.query.filter_by(event_id = event_idd).all()
    
    if not event_users:
        return jsonify({
            "event_id": event.id,
            "event_name": event.name,
            "total_users": 0,
            "users": ["Chưa có ai tham gia sự kiện"]
        }), 200

    users_list = []
    
    for event_user in event_users:
        user = Users.query.get(event_user.user_id)
        if user:
            users_list.append({
                "user_id": user.id,
                "name": user.name,
            })

    return jsonify({
        "event_id": event.id,
        "event_name": event.name,
        "total_users": len(users_list),
        "users": users_list
    }), 200

#8. lấy danh sách chi tiết user từ sự kiện nhất định.
@event_bp.route("/events/<int:event_id>/users/<int:user_id>", methods=["DELETE"])
def delete_detail_user_from_detail_event(event_id,user_id):
    event =Events.query.get(event_id)
    if not event:
        return jsonify({"error":"Không tìm thấy event"}),404
    user_check = Users.query.get(user_id)
    if not user_check:
        return jsonify({"Message":"Không tìm thấy user"})
    Ev_user = Event_User.query.filter_by(event_id=event_id).all()
    if not Ev_user :
        return jsonify({"Message":"Chưa ai tham gia sự kiện"})
    user = Event_User.query.filter_by(event_id=event_id,user_id=user_id).first()
    if not user:
        return jsonify({"Message": "Người dùng không tham gia sự kiện"})
    
    db.session.delete(user)
    try:
        db.session.commit()
        return jsonify({"Message": "Đã xóa thành công"})
    except Exception as ex:
        db.session.rollback()
        return jsonify({
        "error": str(ex)
        })
        
#9. Xóa người dùng tham gia 1 sự kiện.
@event_bp.route("/events/<int:event_id>/users/<int:user_id>", methods=["GET"])
def get_detail_user_from_detail_event(event_id,user_id):
    event =Events.query.get(event_id)
    if not event:
        return jsonify({"error":"Không tìm thấy event"}),404
    user_check = Users.query.get(user_id)
    if not user_check:
        return jsonify({"Message":"Không tìm thấy user"})
    Ev_user = Event_User.query.filter_by(event_id=event_id).all()
    if not Ev_user :
        return jsonify({"Message":"Chưa ai tham gia sự kiện"})
    user = Event_User.query.filter_by(event_id=event_id,user_id=user_id).first()
    if not user:
        return jsonify({"Message": "Người dùng không tham gia sự kiện"})
    return jsonify({
        "event_id": event_id,
        "user": user_check.to_dict()
    })
    
