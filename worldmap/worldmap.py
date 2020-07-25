from django_plotly_dash import DjangoDash # import dashから変更
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash_table.Format import Format, Group, Scheme, Symbol

import pandas as pd
import world_bank_data as wbd


df_gdp_pcap = wbd.get_series('NY.GDP.PCAP.KD', mrv=100)
df_lifeexp = wbd.get_series('SP.DYN.LE00.IN', mrv=100)
df_pops = wbd.get_series('SP.POP.TOTL', mrv=100)
_df = pd.merge(df_gdp_pcap,df_lifeexp, on=['Country', 'Year'])
_df = pd.merge(_df, df_pops, on=['Country', 'Year'])
_df.columns = ['一人当たりGDP(ドル)', '平均寿命(歳)', '人口(人）']
df_all_countries = wbd.get_countries()
df = pd.merge(_df.reset_index(), df_all_countries.reset_index(), left_on='Country', right_on='name')
df = df[df['region'] != 'Aggregates'].reset_index(drop=True)
df = df.drop(['iso2Code','name', 'adminregion', 'incomeLevel', 'lendingType', 'capitalCity', 'longitude','latitude'], axis=1).reset_index(drop=True)
df['Year'] = df['Year'].astype(int)

year_options = [{'label':str(year), 'value':year} for year in df['Year'].unique()]
item_options = [{'label':x, 'value':x} for x in ['一人当たりGDP(ドル)', '平均寿命(歳)', '人口(人）']]
color_options = [
    {'label':c, 'value':c} for c in ['aggrnyl', 'aggrnyl_r', 'agsunset', 'agsunset_r', 
    'algae', 'algae_r', 'amp', 'amp_r', 'armyrose', 'armyrose_r', 
    'balance', 'balance_r', 'blackbody', 'blackbody_r', 'bluered', 'bluered_r', 
    'blues', 'blues_r', 'blugrn', 'blugrn_r', 'bluyl', 'bluyl_r', 
    'brbg', 'brbg_r', 'brwnyl', 'brwnyl_r', 'bugn', 'bugn_r', 'bupu', 'bupu_r', 
    'burg', 'burg_r', 'burgyl', 'burgyl_r', 'cividis', 'cividis_r', 
    'curl', 'curl_r', 'darkmint', 'darkmint_r', 'deep', 'deep_r', 
    'delta', 'delta_r', 'dense', 'dense_r', 'earth', 'earth_r', 'edge', 'edge_r', 
    'electric', 'electric_r', 'emrld', 'emrld_r', 'fall', 'fall_r', 
    'geyser', 'geyser_r', 'gnbu', 'gnbu_r', 'gray', 'gray_r', 'greens', 'greens_r', 
    'greys', 'greys_r', 'haline', 'haline_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 
    'ice', 'ice_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r',
    'magenta', 'magenta_r', 'magma', 'magma_r', 'matter', 'matter_r', 
    'mint', 'mint_r', 'mrybm', 'mrybm_r', 'mygbm', 'mygbm_r', 'oranges', 'oranges_r', 
    'orrd', 'orrd_r', 'oryel', 'oryel_r', 'peach', 'peach_r', 'phase', 'phase_r', 
    'picnic', 'picnic_r', 'pinkyl', 'pinkyl_r', 'piyg', 'piyg_r', 
    'plasma', 'plasma_r', 'plotly3', 'plotly3_r', 'portland', 'portland_r', 
    'prgn', 'prgn_r', 'pubu', 'pubu_r', 'pubugn', 'pubugn_r', 'puor', 'puor_r', 
    'purd', 'purd_r', 'purp', 'purp_r', 'purples', 'purples_r', 'purpor', 'purpor_r', 
    'rainbow', 'rainbow_r', 'rdbu', 'rdbu_r', 'rdgy', 'rdgy_r', 
    'rdpu', 'rdpu_r', 'rdylbu', 'rdylbu_r', 'rdylgn', 'rdylgn_r', 'redor', 'redor_r', 
    'reds', 'reds_r', 'solar', 'solar_r', 'spectral', 'spectral_r', 
    'speed', 'speed_r', 'sunset', 'sunset_r', 'sunsetdark', 'sunsetdark_r', 
    'teal', 'teal_r', 'tealgrn', 'tealgrn_r', 'tealrose', 'tealrose_r', 
    'tempo', 'tempo_r', 'temps', 'temps_r', 'thermal', 'thermal_r', 
    'tropic', 'tropic_r', 'turbid', 'turbid_r', 'twilight',  'twilight_r', 
    'viridis', 'viridis_r', 'ylgn', 'ylgn_r', 'ylgnbu', 'ylgnbu_r','ylorbr', 'ylorbr_r',
    'ylorrd', 'ylorrd_r']
]


app = DjangoDash('WorldMap', add_bootstrap_links=True)# dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) から変更
# dash_bootstrap_componentsを利用する場合には"add_bootstrap_links=True"を追加する
# server = app.serverは削除

app.title = "世界の統計地図"
app.layout = dbc.Container(
    [
        html.Div([
            html.H4("世界の統計地図"),
            html.Div([
                html.P("データ元: 世界銀行")
            ], style={"text-align": "right"}),
            html.Div([
                dcc.Dropdown(
                    id='item-dropdown',
                    options=item_options,
                    value='一人当たりGDP(ドル)'
                )
            ], style={'width':'25%', 'marginLeft':'0%', 'marginRight':'0%', 'display':'inline-block', 'textAlign':'left'}),
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown',
                    options=year_options,
                    value=df['Year'].max()
                )
            ], style={'width':'15%', 'marginLeft':'1%','marginRight':'9%','display':'inline-block', 'textAlign':'left'}),
            html.Div([
                dcc.Dropdown(
                    id='color-dropdown',
                    options=color_options,
                    value='aggrnyl'
                )
            ], style={'width':'20%', 'marginLeft':'30%','marginRight':'0%','display':'inline-block','textAlign':'left'}),            
            dbc.Tabs(
                [
                    dbc.Tab(label='グラフ', tab_id="graph"),
                    dbc.Tab(label='データ', tab_id="data")
                ] ,
                id="tabs",
                active_tab="graph",
                className="mt-2"
            ),
            html.Div(id="tab_content")
        ], className="mt-3 mb-3 text-center")
    ]
)


@app.callback(
    Output("tab_content", "children"),
    [Input("tabs", "active_tab"),
    Input("item-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("color-dropdown", "value")]
)
def render_content(active_tab, item, year, color):

    df_selected = df[df['Year'] == year]
    df_selected = df_selected.sort_values(item, ascending=False).reset_index(drop=True).reset_index()
    df_selected['index'] = df_selected['index'].apply(lambda x: x + 1)

    if active_tab == 'graph':

        tab1_content = html.Div(
            [
                dcc.Graph(
                    id="graph", 
                    figure= go.Figure(
                        data = go.Choropleth(
                            locations=df_selected['id'],
                            z = df_selected[item],
                            colorscale=color,
                            text=df_selected['Country']
                        ),
                        layout = go.Layout(
                            margin = {'t': 10, 'b': 5},
                            height = 500
                        )

                    ),
                ),
                dcc.Graph(
                    id="graph-bar",
                    figure= {
                        'data':[
                            go.Bar(
                                x=df_selected['Country'],
                                y=df_selected[item],
                                marker={
                                    'color': df_selected[item],
                                    'colorscale': color
                                }
                            )
                        ],
                        'layout': go.Layout(
                            margin={'t':5, 'b':150},
                        )
                    }
                )
            ]
        )
        return tab1_content

    elif active_tab == 'data':

        tab2_content = html.Div(
            [
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_selected.columns],
                    data=df_selected.to_dict('records'),
                    style_cell_conditional = [
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Country', 'id', 'region']
                    ],
                    style_data_conditional = [
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                )
            ]
        )
        return tab2_content

    else:
        return None

