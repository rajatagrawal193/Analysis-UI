import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import datetime
import uuid

UNACADEMY_LOGO = "https://static.uacdn.net/production/_next/static/images/logo.svg"


def get_navbar():
    date_picker = dbc.Row(
        [
            dcc.DatePickerRange(
                id='date-picker',
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                start_date=datetime.date.today() - datetime.timedelta(days=31),
                end_date=datetime.date.today(),
                style={'padding': '1px'}
            )

        ],
        no_gutters=True,
        align="center",
        className="navbar-nav ml-auto"
    )
    return dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=UNACADEMY_LOGO, height="20px")),
                        dbc.Col(dbc.NavbarBrand("", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            date_picker,
        ],
        color="dark",
        dark=True,
        style=NAVBAR_STYLE
    )


SIDEBAR_STYLE = {
    "top": -20,
    "background-color": "#343a40",
}

CONTENT_STYLE = {
    "padding-left": "2em",
    "padding-right": "2em"
}

NAVBAR_STYLE = {
    "border-radius": "0px",
    "padding-left": "2em",
    # "margin-bottom": "0px !important"
}


def get_sidebar():
    return html.Div(
        [
            dbc.Nav(
                [

                    html.Br(),
                    dbc.NavItem(dbc.NavLink(
                        "Dashboard", disabled=True, href="#")),
                    # dbc.NavItem(dbc.NavLink("Sleep Time",
                    #                         href="/sleep-time", id="sleep-time")),
                    # dbc.NavItem(dbc.NavLink(
                    #     "Daily Routine", href="/routine", id="routine")),
                    dbc.NavItem(dbc.NavLink(
                        "Work Time", href="/worktime_graphs", id="work_time")),
                    dbc.NavItem(dbc.NavLink(
                        "Mess", href="/mess", id="mess")),
                    dbc.NavItem(dbc.NavLink(
                        "Major Events", href="/major_events", id="major_events")),
                    dbc.NavItem(dbc.NavLink(
                        "Sleep Pattern", href="/sleep_pattern", id="sleep_pattern")),
                    dbc.NavItem(dbc.NavLink(
                        "Workout", href="/workout_graphs", id="workout_events")),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="col col-2",
        style=SIDEBAR_STYLE,
    )


def get_content():
    return html.Div(id="page-content", style=CONTENT_STYLE, className="col col-10")


def get_layout():
    session_id = str(uuid.uuid4())
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(session_id, id='session_id', style={'display': 'none'}),
        dcc.Interval(
            id='interval-component',
            interval=21600 * 1000,  # in milliseconds
            n_intervals=0
        ),
        get_navbar(),
        html.Div(html.Div([
            get_sidebar(),
            get_content()
        ], className="row"), className="container-fluid")
    ])
