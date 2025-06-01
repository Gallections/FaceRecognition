from migration import run_migrations
from models import *
from database import get_connection

conn = get_connection()


# run_migrations(conn)
insert_name(conn, "Brennan", "Johnson")
