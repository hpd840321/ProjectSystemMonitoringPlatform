from typing import List, Optional
from sqlalchemy.orm import Session
from app.interface.api.v1.schemas.server import ServerCreate, ServerUpdate
from app.models.server import Server

class CRUDServer:
    def get(self, db: Session, id: int) -> Optional[Server]:
        return db.query(Server).filter(Server.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Server]:
        return db.query(Server).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ServerCreate) -> Server:
        db_obj = Server(
            name=obj_in.name,
            hostname=obj_in.hostname,
            ip_address=str(obj_in.ip_address),
            os_type=obj_in.os_type,
            os_version=obj_in.os_version,
            cpu_cores=obj_in.cpu_cores,
            memory_size=obj_in.memory_size,
            disk_size=obj_in.disk_size,
            agent_version=obj_in.agent_version
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Server, obj_in: ServerUpdate
    ) -> Server:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

server = CRUDServer() 