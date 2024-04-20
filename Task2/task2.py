import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, select, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite+aiosqlite:///test.db')
base_session = sessionmaker(bind=engine)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)


class UserDataTransferObject(BaseModel):
    id: int
    name: str
    age: int
    email: str


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int) -> UserDataTransferObject:
        statement = select(UserDataTransferObject).where(user_id == UserDataTransferObject.id)
        result_value = await self.db.execute(statement)
        user = result_value.scalar_one_or_none()
        if not user:
            raise ValueError(f'User with id {user_id} does not exist')
        return UserDataTransferObject.from_orm(user)

    async def add(self, user: UserDataTransferObject):
        user = UserModel(**user.model_dump())
        self.db.add(user)
        await self.db.commit()


def init_tables():
    Base.metadata.create_all(engine)


async def add_test_data(db: AsyncSession):
    user_service = UserService(db)
    for i in range(10):
        user_data = UserDataTransferObject(name=f"User {i}", age=i, email=f'test{i}@example.com')
        await user_service.add(user_data)

