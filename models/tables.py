from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

request = Table(
    "request",
    metadata,
    Column("request", String, primary_key=True),
    Column("num", Integer)
)

vacancy = Table(
    "vacancy",
    metadata,
    Column("request", String, ForeignKey("request.request")),
    Column("title", String),
    Column("salary", String),
    Column("city", String),
    Column("company", String),
    Column("experience", String),
    Column("typeofemployment",  String),
    Column("schedule", String),
    Column("viewers_count", String),
    Column("link", String)
)
