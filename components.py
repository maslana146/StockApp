import dash_table
import dash_table.FormatTemplate as FormatTemplate
import plotly.express as px
import plotly.graph_objects as go
from dash_table.Format import Sign
from plotly.subplots import make_subplots

import data


def get_market_table(n=50):
    market_data = data.get_n_top_coins(n)
    market_table = dash_table.DataTable(
        id='market_table',
        data=market_data.to_dict('records'),
        columns=[
            {'id': 'ALTRank', 'name': 'ALTRank', 'type': 'numeric'},
            {'id': 'Galaxy Score', 'name': 'Galaxy Score (PT)',
             'type': 'numeric'},
            {'id': 'Social Score', 'name': 'Social Score (PT)',
             'type': 'numeric'},
            {'id': 'Symbol', 'name': 'Symbol', 'type': 'text'},
            {'id': 'Name', 'name': 'Name', 'type': 'text'},
            {
                'id': 'Price',
                'name': 'Price',
                'type': 'numeric',
                'format': FormatTemplate.money(6),
            },
            {
                'id': 'Volume',
                'name': 'Volume',
                'type': 'numeric',
                'format': FormatTemplate.money(2),
            },
            {
                'id': '24 Hours',
                'name': '24 Hours',
                'type': 'numeric',
                'format': FormatTemplate.percentage(2).sign(Sign.positive),
            },
            {
                'id': '1 Hour',
                'name': '1 Hour',
                'type': 'numeric',
                'format': FormatTemplate.percentage(2).sign(Sign.positive),
            },
            {
                'id': 'Market Cap',
                'name': 'Market Cap',
                'type': 'numeric',
                'format': FormatTemplate.money(0),
            },
        ],
        style_data_conditional=[
            {'if': {'filter_query': '{24 Hours} > 0',
                    'column_id': '24 Hours'}, 'color': 'green',
             'fontWeight': 'bold'},
            {'if': {'filter_query': '{24 Hours} < 0',
                    'column_id': '24 Hours'}, 'color': 'red', 'fontWeight': 'bold'
             },
            {'if': {'filter_query': '{24 Hours} = 0',
                    'column_id': '24 Hours'}, 'color': '#f0f921', 'fontWeight': 'bold'
             },
            {'if': {'filter_query': '{1 Hour} > 0', 'column_id': '1 Hour'},
             'color': 'green', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{1 Hour} < 0', 'column_id': '1 Hour'},
             'color': 'red', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{1 Hour} = 0', 'column_id': '1 Hour'},
             'color': '#f0f921', 'fontWeight': 'bold'},
            {'if': {'row_index': 'odd'},
             'backgroundColor': '#061e44'},
        ],
        style_cell_conditional=[{'if': {'column_id': str('Name')},
                                 'textAlign': 'left'},
                                {
                                    'if': {'column_id': 'Volume'},
                                    'width': '200px',
                                    # 'color': 'blue',
                                    'minWidth': '200px',
                                    'maxWidth': '200px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis', },
                                {'if': {'column_id': (str('Symbol'), str('ALTRank'), str('Galaxy Score'),str('Name'))},
                                 'fontWeight': 'bold',
                                 'textAlign': 'center'},
                                {'if': {'column_id': (str('Social Score'))},
                                 'textAlign': 'center'},
                                ],
        style_header={'backgroundColor': '#13326c',
                      'fontWeight': 'bold',
                      'fontSize': 17,
                      'textAlign': 'center'
                      },
        style_cell={'fontSize': 15,
                    'font-family': 'Lucida Console',
                    'backgroundColor': "#082255",
                    'color': '#e5e9f0',
                    'border': '1px solid #082255'},
        sort_action='native',
        editable=False,
        style_as_list_view=True,
        page_size=5,
        #     fill_width=False
    )
    return market_table


def gen_social_dominance_plot(types, selected_coins):
    df = data.get_n_top_coins(50)
    df = df[df['Symbol'].isin(selected_coins)]
    fig_pie = px.pie(df,
                     values=df[types],
                     names=df['Symbol'],
                     hole=+.5,
                     title=types,
                     color_discrete_sequence=px.colors.sequential.Plasma_r,
                     )

    fig_pie.update_layout(plot_bgcolor='#082255', paper_bgcolor='#082255', font_color='#FFFFFF',
                          margin=dict(t=0,b=0,l=0,r=0))

    fig_scatter = px.scatter(df,
                             x=df['Price'],
                             y=df['Volume'],
                             size=df[types],
                             color=df['Symbol'],
                             hover_name=df['Symbol'],
                             log_y=True,
                             log_x=True,
                             size_max=100,
                             color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig_scatter.update_layout(title=types,
                              # xaxis_title="Price ($)",
                              # yaxis_title="Volume($)",
                              plot_bgcolor='#082255',
                              )

    fig_scatter.update_layout(paper_bgcolor='#082255',
                              font_color='#FFFFFF',
                              xaxis=dict(showgrid=False),
                              yaxis=dict(gridcolor="#0f41a3"),
                              margin=dict(t=50, b=0, l=0, r=0)
                              )
    fig_scatter.update_yaxes(title_text="<b>Volume($)</b>")
    fig_scatter.update_xaxes(title_text="<b>Price ($)</b>")

    return fig_pie, fig_scatter


def gen_coin_plots(coin):
    df_coin_data, details = data.get_coin_data(coin)
    price_fig = go.Figure(data=[go.Candlestick(x=df_coin_data['time'],
                                               open=df_coin_data['open'],
                                               high=df_coin_data['high'],
                                               low=df_coin_data['low'],
                                               close=df_coin_data['close'],
                                               name='{} price'.format(details['symbol']))])

    price_fig.update_layout(title=details['name'],
                            yaxis_tickformat='$',
                            xaxis_title='Date',
                            yaxis_title='Price',
                            )

    price_fig.update_xaxes(title_text='Date',
                           rangeslider_visible=True,
                           rangeselector=dict(buttons=list([dict(count=1,
                                                                 label='1M',
                                                                 step='month',
                                                                 stepmode='backward'),
                                                            dict(count=6,
                                                                 label='6M',
                                                                 step='month',
                                                                 stepmode='backward'),
                                                            dict(count=1,
                                                                 label='YTD',
                                                                 step='year',
                                                                 stepmode='todate'),
                                                            dict(count=1,
                                                                 label='1Y',
                                                                 step='year',
                                                                 stepmode='backward'),
                                                            dict(step='all')]), bgcolor=' #061e44'))
    price_fig.add_trace(go.Scatter(x=df_coin_data['time'],
                                   y=df_coin_data['MA-Low'],
                                   mode='lines',
                                   name='Low-Moving Average',
                                   line={'color': '#ff9100',
                                         'width': 1}))
    price_fig.add_trace(go.Scatter(x=df_coin_data['time'],
                                   y=df_coin_data['MA-High'],
                                   mode='lines',
                                   name='High-Moving Average',
                                   line={'color': '#006eff',
                                         'width': 1}))
    price_fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#e5e9f0',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
            gridcolor="#0f41a3",
            color='#e5e9f0'
        ),
        title={
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_size=30,
        showlegend=True,
        plot_bgcolor='#082255',
        xaxis_rangeslider_visible=False
    )
    price_fig.update_layout(paper_bgcolor='#082255', font_color='#FFFFFF', margin=dict(t=0, b=0, l=0, r=0))

    df_social_coin = data.get_social_coin_data(coin)
    colors = px.colors.sequential.Plasma_r
    social_fig = go.Figure()
    labels = ['unique_url_shares', 'url_shares', 'tweets', 'tweet_spam']
    for j, i in enumerate(labels):
        social_fig.add_trace(go.Scatter(x=df_social_coin['time'], y=df_social_coin[i], mode='lines',
                                        name=labels[j],
                                        line=dict(color=colors[j], width=4),
                                        connectgaps=True,

                                        ))

    social_fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Lucida Console',
                size=12,
                color='#e5e9f0',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
            color='#e5e9f0',
            gridcolor="#0f41a3",
        ),
        autosize=False,
        title="24 hours {} social".format(coin),
        xaxis_title="Date",
        yaxis_title="Number",
        showlegend=True,
        plot_bgcolor='#082255',
        paper_bgcolor='#082255',
        font_color='#e5e9f0',
        margin = dict(t=0, b=0, l=0, r=0)
    )

    social_fig.update_layout(legend=dict(
        yanchor="top",
        y=1.5,
        xanchor="right",
        x=1.1
    ))

    indicator_fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=details['price'],
        title="{} 24 hours".format(details['name']),
        delta={'reference': ((1 + (-1 * (details['percent_change_24h'] / 100))) * details['price']), 'relative': True},

    ))
    indicator_fig.update_layout(
        plot_bgcolor='#082255',
        paper_bgcolor='#082255',
        font_color='#e5e9f0',
        margin = dict(t=0, b=0, l=0, r=0)

    )

    fig_volume = px.bar(df_coin_data[20:],
                        x='time',
                        y='volume',
                        color='volume',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        height=400,
                        )

    fig2 = go.Figure(go.Scatter(x=df_coin_data['time'],
                                y=df_coin_data['MA-Volume'],
                                fill='tonexty',
                                mode='lines',
                                line=dict(width=0,
                                          color='rgb(0,212,255,1)',
                                          ),
                                opacity=0.01,
                                name='MV-Volume',
                                line_shape='spline',
                                ))
    fig_volume.update_yaxes(range=[0, 200000000000])
    fig_volume.add_trace(fig2.data[0])
    fig_volume.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            title="Time",
            tickfont=dict(
                family='Arial',
                size=12,
                color='#e5e9f0',
            ),
        ),
        yaxis=dict(
            title="Volume",
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
            gridcolor="#0f41a3",
            color='#e5e9f0'
        ),
        showlegend=True,
        plot_bgcolor='#082255',
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1,
                    xanchor="right",
                    x=1,
                    ),
        height=300,
        coloraxis_showscale=False,

    )
    fig_volume.update_xaxes(fixedrange=True)
    fig_volume.update_yaxes(fixedrange=True)
    fig_volume.update_traces(
        marker=dict(
            line=dict(
                color='#0d378c')
        )
    )

    fig_volume.update_layout(paper_bgcolor='#082255', font_color='#e5e9f0', margin=dict(t=0, b=0, l=0, r=0))

    return price_fig, social_fig, indicator_fig, fig_volume


def meanwhile():
    df = data.get_global_information(change=6, data_points=182)
    fig_volume = make_subplots(specs=[[{"secondary_y": True}]])
    fig_volume.add_trace(go.Scatter(x=df['time'],
                                    y=df['btc_dominance'],
                                    name='BTC dominance',
                                    line=dict(color='#d8576b',
                                              width=3,
                                              )

                                    ), secondary_y=False)
    fig_volume.add_trace(go.Scatter(x=df['time'],
                                    y=df['altcoin_dominance'],
                                    name='Altcoin dominance',
                                    line=dict(color='#bd3786',
                                              width=3,
                                              )
                                    ), secondary_y=False)
    fig_volume.add_trace(go.Scatter(x=df['time'],
                                    y=df['alt_coin_market_cap'],
                                    name='Altcoin market cap',
                                    line=dict(color='#fdca26',
                                              width=3, )
                                    ), secondary_y=True)
    fig_volume.add_trace(go.Scatter(x=df['time'],
                                    y=df['btc_market_cap'],
                                    name='BTC market cap',
                                    line=dict(color='#f0f921',
                                              width=3, )
                                    ), secondary_y=True)

    fig_volume.update_yaxes(title_text="<b>Dominance</b>", secondary_y=False, showline=False,
                            showgrid=False, )
    fig_volume.update_yaxes(title_text="<b>Market cap</b>", secondary_y=True, showline=False,
                            showgrid=False, )
    fig_volume.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            title="Time",
            tickfont=dict(
                family='Arial',
                size=12,
                color='#e5e9f0',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            gridcolor="#0f41a3",
            color='#e5e9f0'
        ),
        showlegend=True,
        plot_bgcolor='#082255'
    )
    fig_volume.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=1,
                                         xanchor="right",
                                         x=1,
                                         font=dict(size=12, )
                                         ),
                             )
    fig_volume.update_xaxes(fixedrange=True)
    fig_volume.update_layout(paper_bgcolor='#082255', font_color='#e5e9f0', margin=dict(t=0, b=0, l=60, r=60))
    return fig_volume
