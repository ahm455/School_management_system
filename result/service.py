from notification.service import create_notification

def publish_result(result):
    result.is_published = True
    result.save()

    student = result.student

    create_notification(
        user=student,title="Result Published",
        message=f"Your result for {result.course.name} is now available.",type="Result")