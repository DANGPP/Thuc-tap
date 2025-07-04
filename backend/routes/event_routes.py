from flask import Blueprint,jsonify,request, current_app
from models.models import  Events, Users, Event_User
from datetime import datetime
from decimal import Decimal
from celery.result import AsyncResult
from extensions import db
from tasks.send_mail_task import send_email_background

import json
event_bp = Blueprint("event",__name__)

#1.Xem thông tin toàn bộ sự kiện
@event_bp.route('/events', methods=['GET'])
def get_events():
    events = Events.query.order_by(Events.id).all()  # Lấy tất cả dữ liệu từ bảng
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
                total_bill=data.get("total_bill", None),
                id_user_payments=data.get("id_user_payments"),
                status ="Open"
        )
        db.session.add(new_event)
        user = Users.query.get(data.get("id_user_payments"))
        # Thêm user vào event
        new_event_user = Event_User(
            event_id=new_event.id,
            user_id=user.id,
            bonusthem="0",
            bill_due=new_event.total_bill,
            status="Người đã thanh toán",
            id_user_payments= user.id
        )
        db.session.add(new_event_user)
        added_events.append(new_event.to_dict())
    try:
        db.session.commit()
        # adjust_status_user_in_event(new_event.id, user_id)
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
@event_bp.route('/events', methods=["DELETE"])
def delete_event_id():
    data = request.get_json()
    # Kiểm tra nếu request body không hợp lệ
    if not data or "list_del_ev" not in data:
        return jsonify({"error": "Invalid request, missing 'list_del_ev'"}), 400

    list_del_ev = data.get('list_del_ev', [])
    if not list_del_ev:
        return jsonify({"error": "No event IDs provided"}), 400
    for id in list_del_ev:
        try:
            Event_User.query.filter_by(event_id=id).delete()
            Events.query.filter_by(id=id).delete()
        except Exception as ex:
            continue
    try:
        db.session.commit()
        return jsonify({"Message":"delete thanh cong"})
    except Exception as ex:
        return jsonify({"Error":str(ex)})   
  
    
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
    events.id_user_payments = data.get('id_user_payments',events.id_user_payments)
    events.status = data.get('status',events.status )
    
    try:
        db.session.commit()
        return jsonify({"da cap nhat thanh cong ":events.to_dict()})
    except Exception as ex:
        return jsonify(str(ex))
#13 chỉnh sửa status của người tham gia sự kiện
# @event_bp.route('/events/<int:event_id>/users/<int:user_id>', methods=["PUT"])
# def adjust_status_user_in_event(event_id, user_id):
#     event_user = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
#     if not event_user:
#         return jsonify({"error": "Người dùng không tham gia sự kiện"}), 404
#     data = request.get_json()
#     if "status" in data:
#         event_user.status = data.get("status", event_user.status)
#     try:
#         db.session.commit()
#         return jsonify({"message": "Đã sửa status thành công"}), 200
#     except Exception as ex:
#         db.session.rollback()
#         return jsonify({"error": str(ex)}), 500
@event_bp.route("/events/<int:event_id>/users/<int:user_id>", methods=["PUT"])

def update_event_user(event_id, user_id):
    event_user = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
    
    if not event_user:
        return jsonify({
            "error": f"Người dùng với user_id: {user_id} không tham gia sự kiện {event_id} hoặc sự kiện không tồn tại"
        }), 404  
    
    data = request.get_json()

    message_parts = []

    if "bonusthem" in data:
        event_user.bonusthem = data["bonusthem"]
        update_bill_due(event_id)
        message_parts.append("bonus")

    if "status" in data:
        event_user.status = data["status"]
        message_parts.append("status")

    if not message_parts:
        return jsonify({"error": "Không có dữ liệu để cập nhật (bonusthem/status)"}), 400

    try:
        db.session.commit()
        return jsonify({"message": f"Đã sửa {' và '.join(message_parts)} thành công"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 500

#14 lấy status của người dùng trong sự kiện
@event_bp.route('/events/<int:event_id>/users/<int:user_id>', methods=["GET"])
def get_status_user_in_event(event_id, user_id):
    event_user = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
    if not event_user:
        return jsonify({"error": "Người dùng không tham gia sự kiện"}), 404
    return jsonify({
        "event_id": event_id,
        "user_id": user_id,
        "status": event_user.status
    }), 200
#6. Thêm người vào 1 sự kiện
@event_bp.route("/events/<int:event_id>/users", methods=["POST"])
def post_user_to_event(event_id):
    event_check = Events.query.get(event_id)
    if not event_check:
        return jsonify({
            "error":"không tìm thấy event" 
        }),404
    data_user_list = request.get_json()
    added_users = []
    not_added_users = []
    for user_id in data_user_list["list_user"]:
               
        bonusthem = "0"
        # Kiểm tra user có tồn tại không
        User = Users.query.get(user_id)
        if not User:
            not_added_users.append({
                "user_id": user_id,
                "error": "Người dùng không tồn tại"
            })
            continue

        # Kiểm tra xem user đã có trong event chưa
        existing_entry = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
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
            status="UnPaid",
            id_user_payments= event_check.id_user_payments
        )
        db.session.add(new_event_user)
        
        added_users.append({
            "user_id": User.id,
            "event_id": event_id,
            "bonusthem": bonusthem
        })

    try:
        db.session.commit()
        update_bill_due(event_id)

        return jsonify({
            "added_users": added_users,
            "not_added_users": not_added_users
        }), 201
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)+"haha"}), 500

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
                "bill_due": event_user.bill_due,
                "status": event_user.status
            })
    users_list = sorted(users_list, key=lambda x: (x["status"] != "Người đã thanh toán", x["user_id"]))

    return jsonify({
        "event_id": event.id,
        "event_name": event.name,
        "total_users": len(users_list),
        "id_user_payments":event.id_user_payments,
        "tong_thu": event.tong_thu,
        "tien_thua": event.tien_thua,
        "users": users_list
    }), 200

#9. Xóa người dùng tham gia 1 sự kiện.
@event_bp.route("/events/<int:event_id>/users", methods=["DELETE"])
def delete_detail_user_from_detail_event(event_id):
    event =Events.query.get(event_id)
    if not event:
        return jsonify({"error":"Không tìm thấy event"}),404
    data = request.get_json()
    list_del_us = data.get("list_del_us", [])
    for id in list_del_us:
        try:
            Event_User.query.filter_by(event_id = event_id, user_id=id).delete()
        except Exception as ex:
            continue
    
    try:
        db.session.commit()
        update_bill_due(event_id)
        return jsonify({"Message": "Đã xóa thành công"})
    except Exception as ex:
        db.session.rollback()
        return jsonify({
        "error": str(ex)
        })

#8. lấy danh sách chi tiết user từ sự kiện nhất định.     
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
        "user": user_check.to_dict(),
        "status": user.status
    })

# 10. Chỉnh sửa số tiền bonus.
# @event_bp.route("/events/<int:event_id>/users/<int:user_id>", methods=["PUT"])
# def adjust_bonus(event_id, user_id):
#     event_user = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
    
#     if not event_user:
#         return jsonify({
#             "Error": f"Người có user_id: {user_id} không tham gia sự kiện hoặc sự kiện {event_id} không tồn tại"
#         }), 404  
    
#     data = request.get_json()
#     if "bonusthem" in data:
#         event_user.bonusthem = data["bonusthem"]  
#         update_bill_due(event_id)
#     if "status" in data:
#         event_user.status = data["status"]
#     try:
#         db.session.commit()
#         return jsonify({"Message": "Đã sửa bonus thành công"}), 200
#     except Exception as ex:
#         db.session.rollback()  
#         return jsonify({"Error": str(ex)}), 500  

# 11. Cập nhật lại tiền cho mỗi người trong sự kiện
@event_bp.route("/events/<int:event_id>/users", methods=["PUT"])
def update_bill_due(event_id):
    # Kiểm tra sự kiện có tồn tại không
    event = Events.query.get(event_id)
    if not event:
        return jsonify({"error": "Không tìm thấy event"}), 404

    # Kiểm tra tổng tiền có hợp lệ không
    if event.total_bill is None or event.total_bill <= 0:
        return jsonify({"error": "Tổng tiền của sự kiện không hợp lệ"}), 400

    # Lấy danh sách người tham gia sự kiện
    event_users = Event_User.query.filter_by(event_id=event_id).all()
    total_users = len(event_users)

    if total_users == 0:
        return jsonify({"message": "Không có ai tham gia sự kiện"}), 200

    # Xử lý `bonus` và cập nhật `total_bill`
    total_bill = Decimal(event.total_bill)
    total_bill_origin= total_bill
    bonus_them = {}  # {user_id: bonus_amount}
    bonus_percent = {}  # {user_id: bonus_calculated}
    total_bonus_percent_users = 0
    check_paid = True
    for user in event_users:
        if user.status.upper() =="unpaid":
            check_paid = False
        bonus_str= "0"
        if user.bonusthem:
            bonus_str = user.bonusthem.strip() 
        
        if bonus_str.endswith("%"):  # Bonus dạng %
            try:
                percent_value = Decimal(bonus_str.strip('%'))
                bonus_amount = (total_bill_origin * percent_value) / Decimal(100)
                bonus_percent[user.user_id] = bonus_amount
                total_bonus_percent_users += 1
            except ValueError:
                return jsonify({"error": f"Bonus không hợp lệ: {bonus_str}"}), 400
        else:  # Bonus là số thường
            try:
                bonus_amount = Decimal(bonus_str)
                bonus_them[user.user_id] = bonus_amount
            except ValueError:
                return jsonify({"error": f"Bonus không hợp lệ: {bonus_str}"}), 400

        total_bill -= bonus_amount  # Trừ bonus ra khỏi tổng tiền
    
    # Chia đều total_bill mới sau khi trừ bonus
    remaining_users = total_users - total_bonus_percent_users
    if remaining_users <= 0:
        return jsonify({"error": "Không thể chia tiền, số người còn lại không hợp lệ"}), 400
    if total_bill<0:
        total_bill=0
    bill_per_user = Decimal(total_bill / remaining_users)

    # Cập nhật lại `bill_due` cho từng user
    for user in event_users:
        if user.user_id in bonus_percent:
            user.bill_due = bonus_percent[user.user_id]  # Nhận số tiền từ bonus %
        elif user.user_id in bonus_them:
            user.bill_due = bill_per_user + bonus_them[user.user_id]  # Nhận số tiền từ bonus thường
        else:
            user.bill_due = max(bill_per_user, 0)  # Nếu bill_per_user < 0, đặt về 0
    # Cập nhật tổng thu và tiền thừa
    tong_thu =0
    tien_thua = 0
    for user in event_users:
        tong_thu += user.bill_due
    if tong_thu>total_bill_origin:
        tien_thua = tong_thu-total_bill_origin
    event.tong_thu= tong_thu
    event.tien_thua = tien_thua
    if check_paid:
        check_paid = True
        
    try:
        db.session.commit()
        return jsonify({"message": "Đã cập nhật bill_due thành công"}), 200
    except Exception as ex:
        db.session.rollback()
        print("Lỗi cập nhật bill_due:", str(ex))  # Log lỗi để debug
        return jsonify({"error": "Lỗi khi cập nhật bill_due", "details": str(ex)}), 500
#12 gửi mail
@event_bp.route('/events/send-email/<int:event_id>/<int:user_id>', methods=["POST"])
def send_email(event_id,user_id):
    emailUser = Users.query.get(user_id).email_teams
    if not emailUser:
        return jsonify({"error":"emailUser không tồn tại"})
    user = Event_User.query.filter_by(event_id= event_id, user_id = user_id).first()
    if not user:
        return jsonify({"error":"user cần gửi thông báo không tồn tại"})
    event = Events.query.get(event_id)
    usercantratien = Users.query.get(event.id_user_payments)
    if not usercantratien:
        return jsonify({"error":"user cần gửi tiền không tồn tại"})

    if not event:
        return jsonify({"error":"event cho việc tìm người để gửi thông báo không tồn tại"})
    try:
        # mail.send(msg) thay bang code ben duoi
        task= send_email_background.delay(
            subject='Nộp tiền sự kiện',
            recipient=emailUser,
            body=f"""
                Sự kiện: {event.name}
                ID: {event.id}
                Diễn ra vào ngày: {event.date}
                Bạn đã chọn bonus: {user.bonusthem}
                Phải nộp: {user.bill_due} VNĐ
                Vui lòng chuyển khoản đến: {usercantratien.name}       
                        Ngân hàng: {usercantratien.ten_nh}
                        Số tài khoản: {usercantratien.stk}
                """
)
        return jsonify({'message': 'Email sẽ được gửi trong nền (background)',
                        "task_id": task.id
                        }), 202
        # return jsonify({'message': 'Đã gửi mail thành công'}), 200
    except Exception as e:
        return jsonify({'error': "Lỗi ở 12 gửi email"+str(e)}), 500

# 13: lấy id của task celery
@event_bp.route("/task-status/<task_id>")
def get_task_status(task_id):
    task_result = AsyncResult(task_id)
    return jsonify({
        "state": task_result.state,
        "result": str(task_result.result)
    })