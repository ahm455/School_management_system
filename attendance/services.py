from notification.service import create_notification

def mark_absent(attendance):

    create_notification(
        user=attendance.student,
        title="Absent Marked",
        message=f"You were marked absent on {attendance.date} in {attendance.course.name}.",
        type="Attendance"
    )