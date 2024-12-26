from sqlalchemy.orm import Session
from models.log import Log
from datetime import datetime

class LogService:

    def __init__(self, session: Session):
        self.session = session

    def create_log(self, action: str, task_id: int, user_id: int, project_id: int, timestamp: datetime = datetime.utcnow()) -> Log:
        log = Log(timestamp=timestamp, action=action, task_id=task_id, user_id=user_id, project_id=project_id)
        self.session.add(log)
        self.session.commit()
        return log

    def get_log_by_id(self, log_id: int) -> Log:
        return self.session.query(Log).filter(Log.id == log_id).first()

    def get_all_logs(self) -> list[Log]:
        return self.session.query(Log).all()

    def delete_log(self, log_id: int) -> bool:
        log = self.get_log_by_id(log_id)
        if log:
            self.session.delete(log)
            self.session.commit()
            return True
        return False