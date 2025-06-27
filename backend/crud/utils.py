from backend.database import SessionLocal

def with_session(func):
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(session, *args, **kwargs)
            return result
        finally:
            session.close()
    return wrapper