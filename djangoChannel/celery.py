from celery import Celery

worker_hijack_root_logger = False
worker_redirect_stdouts_level = 'INFO'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoChannel.settings')
app = Celery('django_channel', broker='redis://127.0.0.1:6379/2')
# result_backend = 'db+sqlite:///results.db'

result_expires = 0
timezone = 'Asia/Shanghai'
enable_utc = False
task_acks_late = True
worker_max_tasks_per_child = 20  # 每个worker最多执行的任务数
task_soft_time_limit = 30 * 60
task_time_limit = 30 * 60  # 任务超时时间
worker_concurrency = 8
# broker_connection_retry_on_startup = True
# celery-5.3.4

# app.autodiscover_tasks()  # 自动发现task，这个配置会自动从每个app目录下去发现tasks.py文件
