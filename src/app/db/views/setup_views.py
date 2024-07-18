from tortoise import Tortoise


crosstab = "CREATE EXTENSION IF NOT EXISTS tablefunc;"


async def setup_view():
    # get connection
    connection = Tortoise.get_connection(connection_name="default")

    # ************************************************************
    # ******************* View Name ****************
    # ************************************************************
    sql = (
        "SELECT EXISTS (SELECT table_name FROM information_schema.views"
        "WHERE table_name = 'view_name')"
    )
    res = await connection.execute_query(sql)
    status = res[1][0]["exists"]
    if not status:
        await connection.execute_script(crosstab)
        # view not exits; let's create all the views
        # await connection.execute_script(v_jd_history)
