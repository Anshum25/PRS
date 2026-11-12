import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from daily_job import run_daily_automation

PORT = int(os.environ.get("PORT", 8080))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/run-now":
            # Run in a background thread so the HTTP request doesn't timeout
            threading.Thread(target=run_daily_automation).start()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Daily job triggered! Check your WhatsApp in a few seconds.")
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Daily X Post Bot</title></head>
            <body style='font-family:sans-serif; text-align:center; padding-top:50px;'>
                <h2>Daily X Post Engine for @TheAnshumDev</h2>
                <p>Status: <strong>Running & Ready</strong></p>
                <p><a href='/run-now' style='display:inline-block; padding:10px 20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;'>Trigger Delivery to WhatsApp Now</a></p>
            </body>
            </html>
            """)

def background_daily_scheduler(target_hour_utc=3, target_minute_utc=30):
    """Simple lightweight daily loop: checks every 60 seconds if it's trigger time."""
    print(f"⏰ Scheduler active: configured to run daily at {target_hour_utc:02d}:{target_minute_utc:02d} UTC (09:00 AM IST)")
    last_run_day = None
    while True:
        now = time.gmtime()
        current_day = now.tm_yday
        if now.tm_hour == target_hour_utc and now.tm_min == target_minute_utc and last_run_day != current_day:
            print("⏰ Scheduled time hit! Triggering daily job...")
            last_run_day = current_day
            try:
                run_daily_automation()
            except Exception as e:
                print(f"Error in scheduled run: {e}")
        time.sleep(60)

def run_server():
    # Start the scheduler in background thread
    scheduler_thread = threading.Thread(target=background_daily_scheduler, daemon=True)
    scheduler_thread.start()
    
    server = HTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    print(f"🌐 Server running on port {PORT}. Ready for Render deployment.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run_server()
