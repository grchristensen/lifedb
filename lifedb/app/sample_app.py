"""Sample Dash application using example HR data."""

import os
from pathlib import Path

import duckdb
import numpy as np
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html
from dotenv import find_dotenv, load_dotenv

from lifedb import DBError

DATA_SQL = """
select
    emps.employee_id,
    emps.first_name as employee_first_name,
    emps.last_name as employee_last_name,
    emps.email as employee_email,
    emps.phone_number as employee_phone_number,
    emps.hire_date as employee_hire_date,
    jobs.job_title,
    depts.department_name as department,
    locs.street_address as office_address,
    locs.postal_code as office_postal_code,
    locs.city as office_city,
    locs.state_province as office_state_province,
    locs.country_id as office_country_code,
    emps.manager_id,
    mans.first_name as manager_first_name,
    mans.last_name as manager_last_name,
    emps.salary as mo_salary,
    -- Picking a random date in 2005 for interesting tenure.
    date '2005-03-08' as data_as_of_date
from sample.employees as emps
left join sample.jobs
    on emps.job_id = jobs.job_id
left join sample.departments as depts
    on emps.department_id = depts.department_id
left join sample.locations as locs
    on depts.location_id = locs.location_id
left join sample.employees as mans
    on emps.manager_id = mans.employee_id
"""


load_dotenv(find_dotenv())


db_path_str = os.getenv("LIFEDB_DB_PATH")

if db_path_str is None:
    raise KeyError("Missing required environment variable: LIFEDB_DB_PATH")

db_path = Path(db_path_str)

if not db_path.exists():
    raise DBError(f"Database does not exist at {db_path}")

con = duckdb.connect(db_path)

data = con.sql(DATA_SQL).df()

con.close()

data["employee_name"] = data["employee_first_name"] + " " + data["employee_last_name"]
data["tenure"] = (
    data["data_as_of_date"] - data["employee_hire_date"]
) / np.timedelta64(1, "Y")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
sample_app = Dash(external_stylesheets=external_stylesheets)

sample_app.layout = [
    html.H1(children="Employee Registry", style={"textAlign": "center"}),
    dash_table.DataTable(
        data=(
            data[
                [
                    "employee_id",
                    "employee_name",
                    "employee_email",
                    "department",
                    "job_title",
                    "employee_hire_date",
                    "tenure",
                    "mo_salary",
                ]
            ]
        ).to_dict("records"),
        page_size=5,
    ),
    html.Hr(),
    dcc.RadioItems(
        options=["mo_salary", "tenure"],
        value="mo_salary",
        id="controls-and-radio-item",
        inline=True,
    ),
    html.Hr(),
    dcc.Graph(figure={}, id="controls-and-graph"),
]


@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen):
    """Update graph based on desired metric."""
    fig = px.histogram(data, x="department", y=col_chosen, histfunc="avg")
    return fig
