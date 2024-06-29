from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def limit_time(app):
    # Initialize Limiter
  limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
   
  return limiter
