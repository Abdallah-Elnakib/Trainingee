from mongoengine import connect
from models_user import User
from models_track import Track
from models_otp import Otp
from models_student import Student
import datetime

# Connect to MongoDB (default localhost)
connect('your_db_name_here')  # ضع اسم قاعدة البيانات هنا

# إضافة مستخدم جديد
user = User(
    first_name="Ali",
    last_name="Ahmed",
    username="ali123",
    email="ali@example.com",
    password="password123",
    role="student"
)
user.save()
print("User saved!")

# إضافة Track جديد
track = Track(
    track_name="Track 1",
    track_data=[1, 2, 3]
)
track.save()
print("Track saved!")

# إضافة OTP جديد
otp = Otp(
    email="ali@example.com",
    otp="123456",
    created_at=datetime.datetime.utcnow()
)
otp.save()
print("OTP saved!")

# إضافة طالب جديد
student = Student(
    student_id=1,
    name="Mohamed",
    degrees=90,
    additional=10,
    basic_total=100,
    total_degrees=100,
    comments="Excellent"
)
student.save()
print("Student saved!")
