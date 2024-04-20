import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .task2 import Base, UserService, UserDataTransferObject


@pytest.fixture(scope='function')
async def setup_database():
    test_engine = create_async_engine('sqlite+aiosqlite:///test.db', echo=True)
    async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

    test_engine.begin().run_sync(Base.metadata.create_all)

    yield async_session()

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_add_and_get_user(setup_database):
    # Use async with to get an AsyncSession instance
    async with setup_database() as session:
        # Create the user service with the session
        user_service = UserService(session)

    new_user_dto = UserDataTransferObject(name="TestName", age=30, email="TestName@example.com")
    await user_service.add(new_user_dto)

    retrieved_user = await user_service.get(1)

    assert retrieved_user.id == 1
    assert retrieved_user.name == "TestName"
    assert retrieved_user.age == 30
    assert retrieved_user.email == "TestName@example.com"
