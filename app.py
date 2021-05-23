import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_trich_components as dtc
# import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import components
import data

df = data.get_n_top_coins(50)
COINS = df['Symbol'].to_list()
options = []
for coin in COINS:
    options.append({'label': coin, 'value': coin})


def build_header():
    return html.Div([
        html.Div([
            html.H4("Stock App".upper(), className='app-header-title'),
            html.P("Top coins information", 'app-header-subtitle'),
        ], className='app-header-main'),
        html.Img(
            src='assets/logo1.png',
            className='logo'
        ),
        html.Audio(id='easter-egg', controls=True, autoPlay=True, hidden=True)
    ], className='app-header')


def build_tabs():
    return html.Div(
        id='tabs',
        className="tabs",
        children=[
            dcc.Tabs(
                id='control-tabs',
                value='tab1',
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id='Main-tab',
                        label='Market Analysis',
                        value="tab1",
                        className="custom-tabs",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id='Sub-tab',
                        label='Coin Analysis',
                        value="tab2",
                        className="custom-tabs",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id='Rest-tab',
                        label='Add-ons',
                        value="tab3",
                        className="custom-tabs",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def generate_type_dropdown():
    return dcc.Dropdown(id='types',
                        className='dropdown-type',
                        value='Market Dominance',
                        options=[{'label': x,
                                  'value': x,
                                  } for x in ['Market Dominance',
                                              'Social Dominance',
                                              'Number of tweets']],
                        clearable=False,
                        # trzeba pozmieniac jakos na naturalne kolory te dropdowny
                        style={
                            'font-family': 'Lucida Console',
                            'color': '#212121',
                            'border': '0px',

                        })


def generate_symbol_dropdown():
    return dcc.Dropdown(id='selected_coins',
                        className='dropdown-top',
                        value=COINS[:3],
                        options=options,
                        multi=True,
                        style={'color': '#212121',
                               "font-family":'Courier New'
                               # 'display':'flex'
                               # 'border': '2px solid #082255',

                               })


def generate_coin_dropdown():
    return dcc.Dropdown(
        id='coin-dropdown',
        clearable=False,
        value='BTC',
        options=[{'label': c, 'value': c} for c in COINS],
        style={'color': '#212121'})


def build_tab_1():
    return [
        dcc.Loading(id='loading_tab1',
                    children=[
                        html.Div([
                            html.Div([
                                components.get_market_table()],
                                className='tabble-wrapper'),

                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P("Type:"),
                                        generate_type_dropdown(),
                                        html.P("Enter a stock symbol:"),
                                        generate_symbol_dropdown(),
                                    ], className='dropdowns-wrapper'),
                                    html.Div([
                                        dcc.Graph(id="pie-chart", className='dominancePie', responsive='auto')],
                                        className='gauge-wrapper'),

                                ], className='leftcolumn-wrapper'),
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id="scatter-chart", className='marketScatter')],
                                        className='scatter-wrapper'),
                                    html.Div([
                                        dcc.Graph(id='dominance-line', className='dominanceGraph')
                                    ], className='dominance-wrapper')

                                ], className='rightcolumn-wrapper'),
                            ], className='bottom-wrapper')

                        ], className='first-div')], type='cube')
    ]


def build_tab_2():
    return [
        dcc.Loading(id='loading_tab1',
                    children=[
                        html.Div([  # second div
                            html.Div([  # left column
                                html.Div([  # topleft wrapper
                                    html.Div([
                                        html.Label("Coin"),
                                        generate_coin_dropdown()
                                    ], className='dropdowns2-wrapper'),
                                    html.Div([
                                        dcc.Graph(id="indicator", className='indicatorGraph')
                                    ], className='indicator')

                                ], className='topleft-wrapper'),
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='graph-social', className='socialGraph')
                                    ], className='plotline-wrapper'),

                                ], className='bottomleft-wrapper')
                            ], className='leftcolumn2-wrapper'),

                            html.Div([
                                html.Div([
                                    dcc.Graph(id='graph', className='graphGraph')
                                ], className='plotline3-wrapper'),
                                html.Div([
                                    dcc.Graph(id='volumeplot', className='volumeGraph')
                                ], className='volumeplot-wrapper')
                            ], className='rightcolumn2-wrapper')

                        ], className='second-div')], type='cube', style=dict(color="red"))
    ]


def build_card(links, image_path, titles, desc, source, who, symbol):
    return dtc.Card(
        link=links,
        image=image_path,
        title=titles,
        # description=desc,
        badges=[source, who, symbol],
        dark=True
    )


feeds, lists = None, None


def genfeeds():
    global feeds, lists
    feeds = data.get_feeds_information()
    lists = [i for i in range(20)]
    random.shuffle(lists)


def create_card(ids):
    dfo = feeds.iloc[lists[ids]]
    return build_card(dfo['url'], dfo['image'], dfo['title'], dfo['description'],
                      dfo['type'], dfo['publisher'], dfo['symbol'])


def build_tweet(img_src, text, name, second_name, link, time):
    return html.Blockquote([
        html.P(text,
               lang="en",
               dir="ltr"),
        "~ " + name + "(@" + second_name + ")  ",
        html.Img(src=img_src),
        html.A('  ' + time.strftime("%m %B %Y"),
               href=link,
               )
    ], className="twitter-tweet")


def create_tweet(ids):
    feeds = data.get_tweets_data()
    lists = [i for i in range(20)]
    random.shuffle(lists)
    dfo = feeds.iloc[lists[ids]]
    return build_tweet(dfo.profile_image, dfo.body, dfo.display_name, dfo.twitter_screen_name, dfo.url, dfo.time)


def build_tab_3():
    return [
        dcc.Loading(children=[
            html.Div([  # third-div
                html.Div([
                    html.Div([  # card-container
                        html.Div([  # card-box
                            create_card(0),
                        ], className='card-box'),
                        html.Div([  # card-box
                            create_card(1),
                        ], className='card-box'),
                        html.Div([  # card-box
                            create_card(2),
                        ], className='card-box'),
                        html.Div([  # card-box
                            create_card(3),
                        ], className='card-box'),

                    ], className='card-container'),
                ], className='left-container'),
                html.Div([  # right-container
                    html.Div([

                        html.Details([
                            html.Summary("About application:"),
                            html.Div([
                                html.Blockquote([
                                    html.P(
                                        "Application, which is created by young, talentful developer team, by using:"),
                                    html.A("Dash Framework", href='https://dash.plotly.com/'),
                                    html.P("Data is provided by:"),
                                    html.A("LunarCrush Api v2", href='https://lunarcrush.com/'),
                                ])

                            ])
                        ]),
                        html.Details([
                            html.Summary("Young, talentful developers:"),
                            html.Div([
                                html.P(["Bartosz Maślanka ", html.A("Github", href='https://github.com/maslana146'), " ",
                                        html.A("Linkedin",
                                               href='https://www.linkedin.com/in/bartosz-ma%C5%9Blanka-149ba21b0')]),
                                html.P(["Kajetan Kubik ", html.A("Github", href='https://github.com/Imrauviel'), " ",
                                        html.A("Spotify",
                                               href='https://open.spotify.com/user/21k7zbtax556bcwruwsoizeoi?si=f98795e9ef124229')]),
                            ])
                        ]),
                        html.Details([
                            html.Summary("???"),
                            html.Div([
                                html.P("some text")
                            ])
                        ])
                    ], className='AboutUs')
                ], className='right-container')

            ], className='third-div')], type='cube')
    ]


app = dash.Dash(__name__)

app.title = 'Stock app'
server = app.server

app.layout = html.Div([
    html.Div([
        build_header(),
        build_tabs(),
        html.Div(id='app-content')
    ], style={'padding': 20})

])


@app.callback(
    Output('app-content', 'children'),
    Input('control-tabs', 'value')
)
def prepare_top(tab_switch):
    if tab_switch == 'tab1':
        return build_tab_1()
    elif tab_switch == 'tab2':
        return build_tab_2()
    else:
        genfeeds()
        return build_tab_3()


@app.callback(
    [Output("pie-chart", "figure"),
     Output("scatter-chart", "figure")],
    [Input("types", "value"),
     Input('selected_coins', 'value')])
def generate_chart(types, selected_coins):
    return components.gen_social_dominance_plot(types, selected_coins)


@app.callback(
    Output('easter-egg', 'src'),
    Input('coin-dropdown', 'value'))
def easteregg(coin):
    if coin == 'DOGE':
        return 'assets/dog.wav'
    else:
        return ''


@app.callback(
    [Output('graph', 'figure'),
     Output('graph-social', 'figure'),
     Output('indicator', 'figure'),
     Output('volumeplot', 'figure')],
    [Input('coin-dropdown', 'value')]
)
def update_figure(coin):
    return components.gen_coin_plots(coin)


@app.callback(
    Output("dominance-line", "figure"),
    [Input("types", "value"),
     Input('selected_coins', 'value')]
)
def altcoins(types, coin):
    return components.meanwhile()


if __name__ == '__main__':
    app.run_server(debug=True, port=1111)
