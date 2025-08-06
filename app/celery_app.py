"""
Optional Celery configuration for async task processing.
Uncomment and configure when ready to use Celery.
"""

# from celery import Celery
# from app.config import settings

# # Create Celery app
# celery_app = Celery(
#     "api-msj",
#     broker=settings.celery_broker_url,
#     backend=settings.celery_result_backend,
#     include=["app.tasks"]
# )

# # Celery configuration
# celery_app.conf.update(
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     timezone="UTC",
#     enable_utc=True,
#     task_track_started=True,
#     task_time_limit=30 * 60,  # 30 minutes
#     task_soft_time_limit=25 * 60,  # 25 minutes
# )

# # Optional: Configure task routes
# celery_app.conf.task_routes = {
#     "app.tasks.send_email_task": {"queue": "email"},
#     "app.tasks.send_bulk_emails_task": {"queue": "email_bulk"},
# } 