
#This library is used to initialize the dash application.
import dash
from datetime import datetime
# This library is used to add graphs,other visual components.
from dash import dcc
# This library is used to include html tags.
from dash import html
#For data manipulation and mathematical operations.
import pandas as pd
from dash.dependencies import Input, Output 
#Reading the csv file.
data = pd.read_csv("Price_data.csv", skiprows=[0, 2, 3])
data['Equity 1'].fillna(value=data['Equity 1'].mean(), inplace=True)
data["Date"] = data["Date"].apply(lambda x:datetime.strptime(x,"%d-%b-%y").strftime("%Y-%m-%d"))
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
external_stylesheets = [
    {
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Stock Price Analysis"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Stock Price Analysis", className="header-title"
                ),
                html.P(children="Analyze the behavior of Stock prices between 2020 and 2022",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Equity", className="menu-title"),
                        dcc.Dropdown(
                            id="equity-filter",
                            options = ["Equity 1", "Equity 2 ", "Equity 3", "Equity 4"],
                            value="Equity 1",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)



@app.callback(
    Output("price-chart", "figure"),
    [
        Input("equity-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(equity ,start_date, end_date):
    mask = (data.Date >= start_date) & (data.Date <= end_date)
    filtered_data = data.loc[mask, :]
    # end_price = filtered_data[equity].iloc[-1]
    # start_price = filtered_data[equity].iloc[0]
    # price_ratio = end_price/start_price
    # returns = (price_ratio)**(1/(len(filtered_data))/365) - 1
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data[equity],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Stock Price",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return price_chart_figure





if __name__ == '__main__':
    app.run_server(debug=True)
    
    