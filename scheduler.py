# ----------------------------------------------------- #
# --------- This file handles scheduler jobs ---------- #
# ----------------------------------------------------- #
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from background_tasks import update_product_offers, delete_out_of_stock_offers


def init_scheduler(app):
    scheduler = BackgroundScheduler()

    with app.app_context():
        scheduler.add_job(update_product_offers, IntervalTrigger(seconds=5), args=[app])
        scheduler.add_job(delete_out_of_stock_offers, IntervalTrigger(seconds=5), args=[app])

    return scheduler



