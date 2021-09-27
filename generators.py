# We all know about managin connections with classes.
# But how about generators and functions?
# This is working example of handling db connections with generators. 
# All db-related code was cutted for the sake of runing it locally as an example.

def setup_db_and_query(config):
    """Setting up db connection, cursor and performing a query
    """
    # creating connection
    # conn = psycopg2.connect(config)
    # with conn:
    #     with conn.cursor() as curr:
    try:
        while True:
            query = yield
            # do stuff
            # curr.execute(query)
            # accidentally raises psycopg2.InterfaceError, psycopg2.OperationalError
            # raise KeyError # for example
            yield f"this is your query: {query}"
    finally:
        # conn.close()
        print("Closing connection")


def manage_connection():
    """Managin new connection, reconnection and closing connection
    """
    connection = None
    reconnect = False
    try:
        while True:
            if connection and reconnect:
                connection.close()
                connection = None
                print('Reconnection')

            if not connection:
                connection = setup_db_and_query(...)
                connection.send(None)
                print('Creating connection')

            print('Yielding connection')
            reconnect = yield connection
    finally:
        connection.close()


def execute_query(conn_instance, query=None, reconnect=False, second_call=False):
    """Executing query against existing connection
    """
    conn = conn_instance.send(reconnect)
    try:
        result = conn.send(query)
        if not result:
            result = conn.send(query)
    except KeyError: # we catching (psycopg2.InterfaceError, psycopg2.OperationalError) here and trying to reconnect.
        if second_call:
            print('Nothing, that I can do :( ')
            return
        result = execute_query(conn_instance, reconnect=True, second_call=True)
    return result


# begining of the script
connection = manage_connection()
connection.send(None)


QUERY1 = "QUERY1"
result = execute_query(connection, QUERY1)
print(result)

QUERY2 = "QUERY2"
result = execute_query(connection, QUERY2)
print(result)

QUERY3 = "QUERY3"
result = execute_query(connection, QUERY2)
print(result)

connection.close()
