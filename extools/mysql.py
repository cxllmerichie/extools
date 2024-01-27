from typing import Optional, Union, Any, AsyncGenerator
from aiomysql.cursors import DictCursor
from pymysql import err as errors
from contextlib import suppress
import aiomysql

from . import logman, types


class MySQL:
    def __init__(
            self,
            database: str,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: Optional[str] = None,
            logger: Optional[logman.Logger] = logman.logger
    ):
        self.database: str = database
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.pool: Optional[aiomysql.Pool] = None
        self.logger: logman.Logger = logger

    async def create_pool(self) -> bool:
        with suppress(Exception):
            self.pool = await aiomysql.create_pool(
                db=self.database,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
            )
            return True
        return False

    async def close_pool(self) -> bool:
        with suppress(Exception):
            self.pool.close()
            return True
        return False

    async def execute(
            self,
            query: str,
            args: Union[tuple[Any, ...], dict[str, Any], Any] = (),
    ) -> int:
        """
        Executes SQL query and returns the number of affected rows.
        :param query: SQL query to execute.
        :param args: Arguments passed to the SQL query.
        :return: Number of affected rows.
        """
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, self._parse(args))
                    await connection.commit()
                except errors.Error as e:
                    self.logger.exception(e)
                    await connection.rollback()
                return cursor.lastrowid or cursor.rowcount

    async def select(
            self,
            query: str,
            args: Union[tuple[Any, ...], dict[str, Any], Any] = (),
    ) -> AsyncGenerator[types.AttrDict[str, Any], None]:
        """
        Generator that yields rows.
        :param query: SQL query to execute.
        :param args: Arguments passed to the SQL query.
        :return: Yields rows one by one.
        """
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(query, self._parse(args))
                await connection.commit()
                while record := await cursor.fetchone():
                    yield types.AttrDict(record)

    async def one(
            self,
            query: str,
            args: Union[tuple[Any, ...], dict[str, Any], Any] = (),
    ) -> Optional[types.AttrDict[str, Any]]:
        """
        Get a single row or a list of rows from the database.
        :param query: SQL query to execute.
        :param args: Arguments passed to the SQL query.
        :return: A row or a list of rows.
        """
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, self._parse(args))
                    await connection.commit()
                    return types.AttrDict(await cursor.fetchone() or dict())
                except errors.Error as e:
                    self.logger.error(e)

    async def all(
            self,
            query: str,
            args: Union[tuple[Any, ...], dict[str, Any], Any] = (),
    ) -> list[types.AttrDict[str, Any]]:
        """
        Get a single row or a list of rows from the database.
        :param query: SQL query to execute.
        :param args: Arguments passed to the SQL query.
        :return: A row or a list of rows.
        """
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, self._parse(args))
                    await connection.commit()
                    return [types.AttrDict(row) for row in await cursor.fetchall()]
                except errors.Error as e:
                    self.logger.error(e)

    async def count(
            self,
            query: str,
            args: Union[tuple[Any, ...], dict[str, Any], Any] = (),
    ) -> int:
        """
        Executes SQL query and returns the number of affected rows.
        :param query: SQL query to execute.
        :param args: Arguments passed to the SQL query.
        :return: Number of affected rows.
        """
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, self._parse(args))
                    await connection.commit()
                    return cursor.rowcount
                except errors.Error as e:
                    self.logger.error(e)
                    return 0

    @staticmethod
    def _parse(args: Any) -> tuple[Any, ...]:
        return (args,) if not isinstance(args, (tuple, dict)) else args
