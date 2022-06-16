from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import db, UserDb, OrderDb, IngressDb
from uuid import uuid4

# Account Type
CUSTOMER = 0
STORE = 1

# Customer Landing Tab
CUSTOMER_SHOPS = 0
CUSTOMER_DELIVERY = 1

# Store Landing Tab
STORE_INCOMING = 0
STORE_PREPARING = 1
STORE_DELIVERY = 2

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

########################### USER DB ###########################
def create_acc(newName, newEmail, newPassword, newPostalCode, newUnitNumber, accType):
    user = UserDb.query.filter_by(email=newEmail).first()
    if user:
        return False
    
    uuid = uuid4()
    new_acc = UserDb(id = str(uuid),
                     email = newEmail,
                     name = newName,
                     password = generate_password_hash(newPassword, method='sha256'), # password hashing
                     postalCode = newPostalCode,
                     unitNumber = newUnitNumber,
                     accountType = int(accType))
    try:
        db.session.add(new_acc)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def check_login(email, password):
    userAcc = UserDb.query.filter_by(email=email).first()
    
    if not userAcc or not check_password_hash(userAcc.password, password):
        return "invalid login", None

    else:
        return "approved", userAcc

def get_user(id):
    return UserDb.query.get_or_404(id)

def get_all_stores():
    return UserDb.query.filter_by(accountType=STORE).all()

def update_user(id, name, email, postalCode, unitNumber):
    user_to_update = UserDb.query.get_or_404(id)
    
    try:
        user_to_update.name = name
        user_to_update.email = email
        user_to_update.postalCode = postalCode
        user_to_update.unitNumber = unitNumber
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

########################### ORDER DB ###########################

def create_order(id, storeId):
    orderId = uuid4()
    new_order = OrderDb(orderId=str(orderId),
                        customerId=id,
                        storeId=storeId,
                        orderDetails="Something Cool",
                        status=ORDER_SENT)
    try:
        db.session.add(new_order)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_customer_orders(customerId):
    orders = OrderDb.query.filter_by(customerId=customerId).all()
    storeNames = {}
    for order in orders:
        id = order.storeId
        if id not in storeNames:
            newName = UserDb.query.filter_by(id=id).first().name
            storeNames[id] = newName
    return storeNames, orders

def get_store_orders(storeId):
    orders = OrderDb.query.filter_by(storeId=storeId).all()
    customerNames = {}
    print(orders)
    for order in orders:
        print(order)
        id = order.customerId
        if id not in customerNames:
            newName = UserDb.query.filter_by(id=id).first().name
            customerNames[id] = newName
    incoming = OrderDb.query.filter_by(storeId=storeId,
                                      status=ORDER_SENT).all()
    preparing = OrderDb.query.filter_by(storeId=storeId,
                                       status=ORDER_RECEIVED).all()
    delivery = OrderDb.query.filter_by(storeId=storeId,
                                      status=ROBOT_DISPATCHED or 
                                            AT_STORE_HUB or
                                            BETWEEN_HUBS or
                                            AT_DEST_HUB or
                                            ARRIVED).all()
    return customerNames, incoming, preparing, delivery
    

    
def set_order_status(userId, orderId, status):
    order_to_update = OrderDb.query.get_or_404(orderId)

    if order_to_update.storeId == userId or order_to_update.customerId == userId:
        try:
            order_to_update.status = status
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    return False
    
# def get_order(orderId):
#     return OrderDb.query.get_or_404(orderId)

# change order status first then when the other party acknowlege then delete?
# def delete_order(id, orderId):
#     order_to_delete = OrderDb.query.get_or_404(orderId)
#     if order_to_delete.storeId == id:
#         try:
#             db.session.delete(order_to_delete)
#             db.session.commit()
#             return "success"
#         except:
#             return "There was an error deleting the order"
#     else:
#         return "Order does not belong to user"


