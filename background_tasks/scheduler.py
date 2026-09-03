from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


def escalate_pending_requests(app, db, TankerRequest):
    with app.app_context():
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        old_pending_requests = TankerRequest.query.filter(
            TankerRequest.status == 'pending',
            TankerRequest.request_date <= cutoff_time
        ).all()

        count = 0
        for req in old_pending_requests:
            req.urgency_level = 'emergency'
            count = count + 1

        if count > 0:
            db.session.commit()
            print(f"[Background Task] {count} request(s) escalated to emergency.")
        else:
            print("[Background Task] No requests needed escalation.")


def start_scheduler(app, db, TankerRequest):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: escalate_pending_requests(app, db, TankerRequest),
        trigger='interval',
        minutes=1,
        id='escalate_requests_job'
    )
    scheduler.start()
    print("[Background Task] Scheduler started - checking every 1 minute.")