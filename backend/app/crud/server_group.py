from typing import List, Optional
from sqlalchemy.orm import Session
from app.interface.api.v1.schemas.server import ServerGroupCreate
from app.models.server import ServerGroup

class CRUDServerGroup:
    def get(self, db: Session, id: int) -> Optional[ServerGroup]:
        return db.query(ServerGroup).filter(ServerGroup.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ServerGroup]:
        return db.query(ServerGroup).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ServerGroupCreate) -> ServerGroup:
        db_obj = ServerGroup(
            name=obj_in.name,
            description=obj_in.description,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_server_to_group(
        self, db: Session, *, group_id: int, server_id: int
    ) -> ServerGroup:
        group = self.get(db, id=group_id)
        server = crud.server.get(db, id=server_id)
        if not group or not server:
            return None
        group.servers.append(server)
        db.commit()
        db.refresh(group)
        return group

    def remove_server_from_group(
        self, db: Session, *, group_id: int, server_id: int
    ) -> ServerGroup:
        group = self.get(db, id=group_id)
        server = crud.server.get(db, id=server_id)
        if not group or not server:
            return None
        group.servers.remove(server)
        db.commit()
        db.refresh(group)
        return group

server_group = CRUDServerGroup() 