import threading
import time

from core.balancer import start_load_balancer
from core.logger import get_logger

# Optional: Dashboard (Flask)
try:
    from dashboard.stats_server import app as dashboard_app
    DASHBOARD_AVAILABLE = True
except:
    DASHBOARD_AVAILABLE = False


# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger("Main")


# -------------------------------
# Start Load Balancer
# -------------------------------
def run_load_balancer():
    logger.info("Starting Load Balancer...")
    start_load_balancer()


# -------------------------------
# Start Dashboard (Optional)
# -------------------------------
def run_dashboard():
    if not DASHBOARD_AVAILABLE:
        logger.warning("Dashboard not available (Flask not installed or error)")
        return

    logger.info("Starting Dashboard at http://127.0.0.1:5000")
    dashboard_app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# -------------------------------
# Main Entry
# -------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Distributed Load Balancer System...")

    # Start Load Balancer Thread
    lb_thread = threading.Thread(target=run_load_balancer)
    lb_thread.daemon = True
    lb_thread.start()

    # Give LB time to start
    time.sleep(1)

    # Start Dashboard in main thread (Flask needs main thread)
    if DASHBOARD_AVAILABLE:
        run_dashboard()
    else:
        # Keep main thread alive if dashboard not used
        while True:
            time.sleep(5)