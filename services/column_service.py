from sqlalchemy.orm import Session
from models.base import ColumnModel

class ColumnService:

    def __init__(self, session: Session):
        self.session = session

    def create_column(self, title: str) -> ColumnModel:
        column = ColumnModel(title=title)
        self.session.add(column)
        self.session.commit()
        return column

    def get_column_by_id(self, column_id: int) -> ColumnModel:
        return self.session.query(ColumnModel).filter(ColumnModel.id == column_id).first()

    def get_all_columns(self) -> list[ColumnModel]:
        return self.session.query(ColumnModel).all()

    def update_column(self, column_id: int, title: str = None) -> ColumnModel:
        column = self.get_column_by_id(column_id)
        if column:
            if title:
                column.title = title
            self.session.commit()
        return column

    def delete_column(self, column_id: int) -> bool:
        column = self.get_column_by_id(column_id)
        if column:
            self.session.delete(column)
            self.session.commit()
            return True
        return False