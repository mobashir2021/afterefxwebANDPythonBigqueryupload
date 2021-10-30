from datetime import date

from django.db import connection
from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
# import mysql.connector
# from sqlalchemy import create_engine
import math

# db_connection_str = 'mysql+pymysql://devdb:Devdb@786#@3.136.40.143/Integration_DB'
# db_connection = create_engine(db_connection_str)

# dffilter = pd.read_sql('SELECT * FROM s_alpha_table', con=db_connection)
# df = dffilter[dffilter['close_value'].notnull()]


# dfFullStocks = pd.read_sql('SELECT * FROM s_snp500_stock_all', con=db_connection)

# dfRedditTwitter = pd.read_sql('SELECT * FROM s_reddit_twitter', con=db_connection)

# dfInfo = pd.read_sql('SELECT * FROM predict_info', con=db_connection)

from .models import Snp500StockDaily, RedditDailyData, PredictInfo, TwitterDailyData, AdWikiPgviews

query = str(Snp500StockDaily.objects.all().query)
dfFullStocks = pd.read_sql_query(query, connection)

query = str(RedditDailyData.objects.all().query)
dfReddit = pd.read_sql_query(query, connection)

query = str(TwitterDailyData.objects.all().query)
dfTwitter = pd.read_sql_query(query, connection)

query = str(PredictInfo.objects.all().query)
dfInfo = pd.read_sql_query(query, connection)

query1 = str(AdWikiPgviews.objects.all().query)
dfWiki = pd.read_sql_query(query1, connection)

listofstocks = ['COST', 'DD', 'LOW', 'SEE', 'VIAC', 'WELL']
listofstockname = ["Costco Wholesale Corp." "DuPont de Nemours Inc", "Lowe's Cos.",
                   "Sealed Air", "ViacomCBS", "Welltower Inc."]

listSector = ['Consumer Staples', 'Materials', 'Consumer Discretionary', 'Communication Services', 'Real Estate']
listSubIndustry = ['Hypermarkets & Super Centers', 'Specialty Chemicals', 'Home Improvement Retail', 'Paper Packaging',
                   'Movies & Entertainment', 'Health Care REITs']

dictStocks = {"Costco Wholesale Corp.": "COST", "DuPont de Nemours Inc": "DD", "Lowe's Cos.": "LOW",
              "Sealed Air": "SEE", "ViacomCBS": "VIAC", "Welltower Inc.": "WELL"}

all_options = {
    'Consumer Staples': {
        'Hypermarkets & Super Centers': ['Costco Wholesale Corp.']
    },
    'Materials': {
        'Specialty Chemicals': ['DuPont de Nemours Inc'],
        'Paper Packaging': ['Sealed Air'],
    },
    'Consumer Discretionary': {
        'Home Improvement Retail': ["Lowe's Cos."]

    },
    'Communication Services': {
        'Movies & Entertainment': ['ViacomCBS']
    },
    'Real Estate': {
        'Health Care REITs': ['Welltower Inc.']
    }
}


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('mygraph', external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.append_css({"external_url": "/static/assets/css/customstyle.css"})

app.layout = html.Div([
    html.Div(children=[
        html.Div([
            html.Div([
                html.H3(id="tickername", children="Ticker Name", style={'color': '#ffffff', 'padding-top': '20px'})
            ], className='col-md-3'),
            html.Div(children=[], className='col-md-6'),
            html.Div(children=[

                html.Img(src='/static/assets/img/outline orange_white n Orange.png', height=48, width=100,
                         style={'float': 'right', 'padding-top': '10px'})
            ], className='col-md-3')
        ], className='row', style={'height': '100px'}),
        html.Div(children=[

            html.Div(children=[
                dcc.Dropdown(
                    id='sector-dropdown',
                    options=[{'label': k, 'value': k} for k in all_options.keys()],
                    value='Consumer Staples',
                    style={'background-color': '#23333A', 'color': '#A1A8AB'}
                )
            ], className='col-md-4'),
            html.Div(children=[
                dcc.Dropdown(
                    id='subindustry-dropdown',
                    style={'background-color': '#23333A', 'color': '#A1A8AB'}
                )
            ], className='col-md-4'),
            html.Div(children=[
                dcc.Dropdown(
                    id='stock-dropdown',
                    style={'background-color': '#23333A', 'color': '#A1A8AB'}
                )
            ], className='col-md-4')
        ], className='row', style={'height': '60px', 'background-color': '#23333A'}),

        html.Div(children=[
            html.Div(children=[
                # dcc.Graph(
                #     id="modelscore",
                #     style={'height': '300px'}
                #
                # )
                html.Div(children=[
                    html.Div(children=[
                        html.H4(children="Model Score", style={'color': '#A1A8AB', 'font': '24px Arial, sans-serif'})
                    ], className="box-title", style={'margin-top': '30px'}),
                    html.Div(children=[
                        html.Div(children=[
                            html.Label(id="modelscore", style={'color': '#FFFFFF', 'margin-top': '24px'})
                        ], className='circle', style={'margin-top': '5px'})

                    ], className="box-text", style={'margin-top': '4%', 'margin-left': '30%'})
                ], className="box", style={'text-align': 'center'})

            ], className='col-md-4', style={'border': '1px solid #A1A8AB'}),
            html.Div(children=[

                html.Div(
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Label(children="Sharpe Ratio    =      ", style={'color': '#A1A8AB'}),
                        html.Label(id="sharperatio", style={'color': '#A1A8AB'})
                    ],
                    style={'height': '100px', 'border': '1px solid #A1A8AB'}
                ),
                html.Div(

                    children=[
                        html.Br(),
                        html.Br(),
                        html.Label(children="Sortino Ratio   =     ", style={'color': '#A1A8AB'}),
                        html.Label(id="sortinoratio", style={'color': '#A1A8AB'})
                    ],
                    style={'height': '100px', 'border': '1px solid #A1A8AB'}
                ),
                html.Div(
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Label(children="Std Deviation   =     ", style={'color': '#A1A8AB'}),
                        html.Label(id="standarddeviation", style={'color': '#A1A8AB'})
                    ],
                    style={'height': '100px', 'border': '1px solid #A1A8AB'}
                )

            ], className='col-md-2', style={'height': '300px'}),
            html.Div(children=[

                dcc.Graph(
                    id="feature",
                    style={'height': '300px'}

                )

            ], className='col-md-4', style={'border': '1px solid #A1A8AB', 'height': '300px'}),
            html.Div(children=[
                html.Br(),

                html.H5(children="Model Info", style={'color': '#A1A8AB', 'font': '24px Arial, sans-serif'}),
                html.Br(),
                html.Br(),
                html.Div(
                    children=[
                        html.Label(children="Tickers :", style={'color': '#A1A8AB'}),
                        html.Label(id="tickernamesc", children="", style={'color': '#A1A8AB', 'margin-left': '40px'})]
                ),
                html.Div(
                    children=[
                        html.Label(children="Model :", style={'color': '#A1A8AB'}),
                        html.Label(children="Model 1", style={'color': '#A1A8AB', 'margin-left': '40px'})]
                ),
                html.Div(
                    children=[
                        html.Label(children="Datasource :", style={'color': '#A1A8AB'}),
                        html.Label(children="Various", style={'color': '#A1A8AB', 'margin-left': '10px'})]
                )

            ], className='col-md-2',
                style={'height': '300px', 'background-color': '#23333A', 'border': '1px solid #A1A8AB'})

        ], className='row', style={'height': '300px'}),

        html.Div(children=[
            html.Div(children=[], className='col-md-4'),
            html.Div(children=[], className='col-md-4'),
            html.Div(children=[
                dcc.DatePickerRange(
                    id='alterdaterange',
                    min_date_allowed=date(2016, 8, 5),
                    max_date_allowed=date.today(),
                    # initial_visible_month=date.today().month,
                    end_date=date.today(),
                    start_date=date(2021, 2, 20)
                )
            ], className='col-md-4')

        ], className='row'),

        html.Div(children=[
            dcc.Graph(
                id="predictiongraph",
                style={'width': '100%'}
            )
        ], className='row', style={'height': '450px', 'border': '1px solid #A1A8AB'}),

        # html.Div(children=[
        #     html.Div(children=[
        #         dcc.Graph(
        #             id="wikigraph",
        #             style={'width': '100%'}
        #         )
        #     ], className='col-md-4', style={'border': '1px solid #A1A8AB'}),
        #     html.Div(children=[
        #         dcc.Graph(
        #             id="redditgraph",
        #             style={'width': '100%'}
        #         )
        #     ], className='col-md-4', style={'border': '1px solid #A1A8AB'}),
        #     html.Div(children=[
        #         dcc.Graph(
        #             id="twittergraph",
        #             style={'width': '100%'}
        #         )
        #     ], className='col-md-4', style={'border': '1px solid #A1A8AB'})
        #
        # ], className='row', style={'height': '450px'}),
        html.Div(children=[
            dcc.Graph(
                id="wikigraph",
                style={'width': '100%'}
            )
        ], className='row', style={'height': '450px', 'border': '1px solid #A1A8AB'}),
        html.Div(children=[
            dcc.Graph(
                id="redditgraph",
                style={'width': '100%'}
            )
        ], className='row', style={'height': '450px', 'border': '1px solid #A1A8AB'}),
        html.Div(children=[
            dcc.Graph(
                id="twittergraph",
                style={'width': '100%'}
            )
        ], className='row', style={'height': '450px', 'border': '1px solid #A1A8AB'}),
        html.Div(children=[
            html.Div(children=[
                # dcc.DatePickerRange(
                #     id='tickerdaterange',
                #     min_date_allowed=date(2016, 8, 5),
                #     max_date_allowed=date.today(),
                #     # initial_visible_month=date.today().month,
                #     end_date=date.today(),
                #     start_date=date(2021, 4, 28)
                # )
            ], className='col-md-4'),
            html.Div(children=[], className='col-md-4'),
            html.Div(children=[
                dcc.Dropdown(
                    id='vol-dropdown',
                    options=[
                        {'label': 'CLOSE', 'value': 'close_value'},
                        {'label': 'OPEN', 'value': 'open_value'},
                        {'label': 'VOLUME', 'value': 'volume'},
                        {'label': 'HIGH', 'value': 'high_value'},
                        {'label': 'LOW', 'value': 'low_value'}
                    ],
                    value='volume',
                    style={'background-color': '#23333A', 'color': '#A1A8AB'}
                )
            ], className='col-md-4')

        ], className='row', style={'height': '90px'}),
        html.Div(children=[
            dcc.Graph(
                id="seriesgraph",
                style={'width': '100%'}
            )
        ], className='row', style={'height': '500px', 'border': '1px solid #A1A8AB'})
    ], className='container', style={'background-color': '#23333A'})

], style={'background-color': '#23333A'})


@app.callback(
    Output('subindustry-dropdown', 'options'),
    [Input('sector-dropdown', 'value')])
def set_cities_options(sectorvalues):
    return [{'label': i, 'value': i} for i in all_options[sectorvalues]]


@app.callback(
    Output('subindustry-dropdown', 'value'),
    [Input('subindustry-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('stock-dropdown', 'options'),
    [Input('sector-dropdown', 'value'),
     Input('subindustry-dropdown', 'value')])
def set_landmarks_options(sectorvalue, subindustryvalue):
    return [{'label': i, 'value': dictStocks[i]} for i in all_options[sectorvalue][subindustryvalue]]


@app.callback(
    Output('stock-dropdown', 'value'),
    [Input('stock-dropdown', 'options')])
def set_landmarks_value(available_options):
    return available_options[0]['value']


# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('stock-dropdown', 'value')])
# def update_output(value):
#     dfstock = df[df['stockid'] == value]
#     dataset = dfstock.copy()
#
#     dataset["date"] = pd.to_datetime(dataset.date)
#     dataset.sort_values("date", inplace=True)
#     dttemp = dataset.tail(1)
#     labels = ['score']
#     values = dttemp.iloc[0]['model_score']
#     return 'You have selected "{}"'.format(dttemp.iloc[0]['close_value'])


@app.callback(
    Output('tickername', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputTicker(value):
    # dfstock = dfFullStocks[dfFullStocks['stockid'] == value]
    # dataset = dfstock.copy()
    #
    # dataset["date"] = pd.to_datetime(dataset.date)
    # dataset.sort_values("date", inplace=True)
    # dttemp = dataset.tail(1)

    return value + ' - Insights'


@app.callback(
    Output('tickernamesc', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputTickersc(value):
    # dfstock = dfFullStocks[dfFullStocks['stockid'] == value]
    # dataset = dfstock.copy()
    #
    # dataset["date"] = pd.to_datetime(dataset.date)
    # dataset.sort_values("date", inplace=True)
    # dttemp = dataset.tail(1)

    return value


@app.callback(
    Output('modelscore', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputTickerModelvalues(value):
    dfstock = dfInfo[dfInfo['stockid'] == value]
    dataset = dfstock.copy()

    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    dttemp = dataset.tail(1)
    lbl = ['score', 'error']
    vls = []
    mdscore = dttemp.iloc[0]['model_score']
    # if mdscore > 100:
    #     mdscore = roundup(mdscore) - mdscore

    # errscore = 100.0 - mdscore
    # # mdscore = 100.0
    # # errscore = 0.0
    # vls.append(mdscore)
    # vls.append(errscore)
    #
    # figure = {
    #     'data': [
    #         go.Pie(
    #             labels=lbl,
    #             values=vls,
    #             hole=.3,
    #             textposition="inside"
    #         )
    #     ],
    #     'layout': go.Layout(
    #         title="Model Score",
    #         # template='plotly_dark'
    #         plot_bgcolor='rgba(35,51,58,1)',
    #         paper_bgcolor='rgba(35,51,58,1)'
    #     )
    # }
    return mdscore


# @app.callback(
#     dash.dependencies.Output('stockvals', 'children'),
#     [dash.dependencies.Input('stock-dropdown', 'value')])
# def update_outputSharperatio(value):
#     return value


@app.callback(
    Output('sharperatio', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputSharperatio(value):
    dfstock = dfInfo[dfInfo['stockid'] == value]
    dataset = dfstock.copy()

    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    dttemp = dataset.tail(1)

    sharperatio = dttemp.iloc[0]['sharpe_ratio']

    return sharperatio


@app.callback(
    Output('sortinoratio', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputSortinoratio(value):
    dfstock = dfInfo[dfInfo['stockid'] == value]
    dataset = dfstock.copy()

    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    dttemp = dataset.tail(1)

    sortinoratio = dttemp.iloc[0]['sortino_ratio']

    return sortinoratio


@app.callback(
    Output('standarddeviation', 'children'),
    [Input('stock-dropdown', 'value')])
def update_outputSortinoratio(value):
    dfstock = dfInfo[dfInfo['stockid'] == value]
    dataset = dfstock.copy()

    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    dttemp = dataset.tail(1)

    standarddeviation = dttemp.iloc[0]['stan_dev']

    return standarddeviation


def SetColor(y):
    if (y == 100):
        return "#59A14F"
    elif (y == 30):
        return "#9C755F"
    elif (y == 50):
        return "#EDC948"


@app.callback(
    Output('feature', 'figure'),
    [Input('stock-dropdown', 'value')])
def update_outputFeatures(value):
    x = [20, 30, 50]
    y = ['Twitter', 'RedditMention', 'WikiPageView']
    # customscale = [[20, "#59A14F"],
    #                [30, "#9C755F"],
    #                [50, "#EDC948"]]
    #
    # dffDataframe = pd.DataFrame(
    #     {'value': x,
    #      'texttitle': y
    #      })
    figuresdata = {
        'data': [
            go.Bar(
                x=x,
                y=y,
                orientation='h',
                marker=dict(color=['#59A14F', '#9C755F', '#EDC948']),
                textposition="auto"
            )
        ],
        'layout': go.Layout(
            title="Model Weights",
            titlefont=dict(
                family='Arial, sans-serif',
                size=24,
                color='#A1A8AB'
            ),
            # template='plotly_dark'

            plot_bgcolor='rgba(35,51,58,1)',
            paper_bgcolor='rgba(35,51,58,1)',
            showlegend=False,
            xaxis=dict(
                title='',
                # titlefont=dict(
                #     family='Courier New, monospace',
                #     size=18,
                #     color='#7f7f7f'
                # ),
                color='#A1A8AB'
            ),
            yaxis=dict(
                title='',
                # titlefont=dict(
                #     family='Courier New, monospace',
                #     size=18,
                #     color='#7f7f7f'
                # )
                color='#A1A8AB'
            )

        )
    }
    # figuresdata = px.bar(dffDataframe, x="value", y="texttitle", orientation='h')
    # figuresdata.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)',
    #                              title='Model Weights', font_color="#A1A8AB",
    #                             title_font_color="#A1A8AB", legend_title_font_color="#A1A8AB")

    return figuresdata


@app.callback(
    Output('predictiongraph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('alterdaterange', 'start_date'),
     Input('alterdaterange', 'end_date')])
def update_outputprediction(value, start_date, end_date):
    dfstock = dfFullStocks[dfFullStocks['stockid'] == value]

    dfMainInfostock = dfInfo[dfInfo['stockid'] == value]

    dataset = dfstock.copy()

    # for index, dd, pv in dfMainInfostock[['date', 'predicted_value']].itertuples():
    #     tempredvalue = pv
    #
    #     tempdate = dd
    #
    #     for tidx, tdate, tpv in dfstock[['date', 'predicted_value']].itertuples():
    #         if tdate == tempdate:
    #             dfstock.at[tidx, 'predicted_value'] = tempredvalue
    # dfstock.replace(0, np.nan, inplace=True)
    dataset = dfstock.copy()
    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    # dttemp = dataset.tail(45)
    dttemp = dataset[(dataset['date'] >= pd.to_datetime(start_date)) & (dataset['date'] <= pd.to_datetime(end_date))]
    x = [20, 14, 23, 19]
    y = ['Wikiview', 'RedditMention', 'Twitter', 'Facebook']
    figtemp = px.line(dttemp, x="date", y="close_value", height=400)
    figtemp.add_scatter(x=dfMainInfostock['date'], y=dfMainInfostock['predicted_value'], mode='lines',
                        line=dict(color="#F28E2B"), name='Predicted Value')
    # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
    figtemp.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)', yaxis={'title': 'Close'},
                          xaxis={'title': 'Date'}, title='Prediction Graph', font_color="#86bcb6",
                          title_font_color="#86bcb6", legend_title_font_color="#86bcb6")
    figtemp.update_xaxes(showgrid=False, linewidth=1)
    figtemp.update_yaxes(showgrid=False, linewidth=1)
    figtemp.update_traces(mode="lines+markers")
    return figtemp


@app.callback(
    Output('seriesgraph', 'figure'),
    [Input('vol-dropdown', 'value'),
     Input('stock-dropdown', 'value'),
     Input('alterdaterange', 'start_date'),
     Input('alterdaterange', 'end_date')])
def update_outputvolume(value, value1, start_date, end_date):
    dfstock = dfFullStocks[dfFullStocks['stockid'] == value1]

    dataset = dfstock.copy()
    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    # print(dataset[(dataset['date'] > pd.to_datetime(start_date)) & (dataset['date'] < pd.to_datetime(end_date))])
    # dttemp = dataset.tail(45)
    dttemp = dataset[(dataset['date'] >= pd.to_datetime(start_date)) & (dataset['date'] <= pd.to_datetime(end_date))]
    figtemp1 = px.line(dttemp, x="date", y=value, height=400)

    # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
    figtemp1.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)', yaxis={'title': 'Value'},
                           xaxis={'title': 'Date'}, title='Tickers Data Graph', font_color="#A1A8AB",
                           title_font_color="#86bcb6", legend_title_font_color="#A1A8AB")
    figtemp1.update_xaxes(showgrid=False, linewidth=2)
    figtemp1.update_yaxes(showgrid=False, linewidth=2)
    figtemp1.update_traces(line_color='#636EFA', mode="lines+markers")

    return figtemp1


@app.callback(
    Output('wikigraph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('alterdaterange', 'start_date'),
     Input('alterdaterange', 'end_date')])
def update_outputwiki(value, start_date, end_date):
    dfstock = dfWiki[dfWiki['stockid'] == value]

    dataset = dfstock.copy()
    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    # print(dataset[(dataset['date'] > pd.to_datetime(start_date)) & (dataset['date'] < pd.to_datetime(end_date))])
    # dttemp = dataset.tail(45)
    dttemp = dataset[(dataset['date'] >= pd.to_datetime(start_date)) & (dataset['date'] <= pd.to_datetime(end_date))]
    figtempwiki = px.line(dttemp, x="date", y="pageviews", height=400)

    # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
    figtempwiki.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)',
                              xaxis={'title': 'Date'},
                              yaxis={'title': "Wiki Pageviews"}, title='Daywise - Wiki', font_color="#A1A8AB",
                              title_font_color="#86bcb6", legend_title_font_color="#A1A8AB")
    figtempwiki.update_xaxes(showgrid=False, linewidth=2)
    figtempwiki.update_yaxes(showgrid=False, linewidth=2)
    figtempwiki.update_traces(line_color='#F28E2B', mode="lines+markers")
    return figtempwiki


@app.callback(
    Output('redditgraph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('alterdaterange', 'start_date'),
     Input('alterdaterange', 'end_date')])
def update_outputreddit(value, start_date, end_date):
    dfstock = dfReddit[dfReddit['stockid'] == value.lower()]

    dataset = dfstock.copy()
    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    # print(dataset[(dataset['date'] > pd.to_datetime(start_date)) & (dataset['date'] < pd.to_datetime(end_date))])
    # dttemp = dataset.tail(45)

    # dataset = dataset[dataset.date.notnull()]
    # print(dataset)
    dttemp = dataset[(dataset['date'] >= pd.to_datetime(start_date)) & (dataset['date'] <= pd.to_datetime(end_date))]

    figtempreddit = px.line(dttemp, x="date", y="redditmention", height=400)

    # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
    figtempreddit.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)',
                                xaxis={'title': 'Date'},
                                yaxis={'title': "Reddit Mention"}, title='Daywise - Reddit', font_color="#A1A8AB",
                                title_font_color="#86bcb6", legend_title_font_color="#A1A8AB")
    figtempreddit.update_xaxes(showgrid=False, linewidth=2)
    # figtempreddit.update_yaxes(showgrid=False, linewidth=3, linecolor='#8EB4FF')
    figtempreddit.update_yaxes(showgrid=False, linewidth=2)
    figtempreddit.update_traces(line_color='#F28E2B', mode="lines+markers")
    return figtempreddit


@app.callback(
    Output('twittergraph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('alterdaterange', 'start_date'),
     Input('alterdaterange', 'end_date')])
def update_outputtwitter(value, start_date, end_date):
    dfstock = dfTwitter[dfTwitter['stockid'] == value.lower()]

    dataset = dfstock.copy()
    dataset["date"] = pd.to_datetime(dataset.date)
    dataset.sort_values("date", inplace=True)
    # print(dataset[(dataset['date'] > pd.to_datetime(start_date)) & (dataset['date'] < pd.to_datetime(end_date))])
    # dttemp = dataset.tail(45)
    dttemp = dataset[(dataset['date'] >= pd.to_datetime(start_date)) & (dataset['date'] <= pd.to_datetime(end_date))]
    figtemptwitter = px.line(dttemp, x="date", y="twitterfollower", height=400)

    # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
    figtemptwitter.update_layout(plot_bgcolor='rgba(35,51,58,1)', paper_bgcolor='rgba(35,51,58,1)',
                                 xaxis={'title': 'Date'},
                                 yaxis={'title': "Twitter Follower"}, title='Daywise - Twitter', font_color="#A1A8AB",
                                 title_font_color="#86bcb6", legend_title_font_color="#A1A8AB")
    figtemptwitter.update_xaxes(showgrid=False, linewidth=2)
    figtemptwitter.update_yaxes(showgrid=False, linewidth=2)
    figtemptwitter.update_traces(line_color='#F28E2B', mode="lines+markers")

    return figtemptwitter


# @app.callback(
#     dash.dependencies.Output('seriesgraph', 'figure'),
#     [dash.dependencies.Input('vol-dropdown', 'value'),
#      dash.dependencies.Input('stock-dropdown', 'value')])
# def update_outputWikipage(value, value1):
#     dfstock = dffilter[dffilter['stockid'] == value1]
#
#     dataset = dfstock.copy()
#     dataset["date"] = pd.to_datetime(dataset.date)
#     dataset.sort_values("date", inplace=True)
#     dttemp = dataset.tail(45)
#
#     figtemp1 = px.line(dttemp, x="date", y=value, height=400)
#
#     # figtemp = px.line(dttemp, x = "date", y="close_value", color="predicted_value", height=400)
#     figtemp1.update_layout(yaxis={'title': value}, title='Data Graph')
#
#     return figtemp1


""" if __name__ == '__main__':
    app.run_server(debug=True) """
