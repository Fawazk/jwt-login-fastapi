from sqlmodel import create_engine, Session

sqlite_file_name = "sqlmodeltest"
sqlite_url = f"postgresql://postgres:postgres@172.17.0.1:5433/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)


def get_db():
    db = Session(engine)
    return db
