import pika


def create_connection(host, username, password):
    credentials = pika.PlainCredentials(username, password)
    conn_params = pika.ConnectionParameters(host='localhost',
                                            credentials=credentials)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    return connection, channel
