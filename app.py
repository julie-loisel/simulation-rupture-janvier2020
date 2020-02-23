# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

import fromage
import plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import random
from plotly.offline import init_notebook_mode, iplot

from fromage import *
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#colors ={'background':'#111111','text':'#7FDBFF'}
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
image_filename = 'assets/palette.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
app.config['suppress_callback_exceptions']=True

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview"
)

app.layout = \
        html.Div([ ### Main contener

html.Div([ # HEADER
                html.Div(#LOGO
                    [
                        html.Img(
                            src=app.get_asset_url("logoINRAE.png"),
                            id="plotly-image",
                            style={
                                "height": "30px",
                                "width": "auto",
                                "margin-top": "25px",
                                "margin-right": "25px"
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Temperature abuse simulation",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Second version", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/julie-loisel/simulation-rupture-janvier2020/tree/new",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "35px"},
        ),

    html.Div([
        #############Coté gauche###########
    dcc.Markdown('''### Construction de la palette'''),
    dcc.Markdown('''Deuxième version d'une application implémentée en Python par Julie Loisel
    utilisant le modèle codé en Matlab par Denis Flick (AgroParisTech)
    et repris par Steven Duret(IRSTEA).
    '''),
    dcc.Markdown(id='affichage_C_vent',style={'font-size':'170%'}),
    dcc.Slider(
        id='C_vent',
        min=0.,
        max=3,
        step=0.01,
        value=1.,
        className="dcc_control"),

    dcc.Markdown(id='affichage_Vfr',style={'font-size':'170%'}),
    dcc.Slider(
        id='Vfr',
        min=0,
        max=3,
        step=0.1,
        value=0.31,
        className="dcc_control"),

    dcc.Markdown(id='affichage_Q',style={'font-size':'170%'}),

    dcc.Slider(
        id='Q',
        min=0.,
        max=1.,
        step=0.02,
        value=0.04,
        className="dcc_control"
        ),
dcc.Markdown('''###### Calculer la conduction'''),
        dcc.RadioItems(id='conduction_bool',
            options=[
                {'label': 'Oui', 'value': 1},
                {'label': 'Non', 'value': 0},

            ],
            value=1,
        className="dcc_control"
        ),
dcc.Markdown('''###### Sources de données pour les lois de distribution'''),

        dcc.RadioItems(id='donnees',
                       options=[
                           {'label': "ANIA", 'value': 'ANIA'},
                           {'label': "Morelli and Derens (2009)", 'value': 'derens_2009'}
                       ],
                       value='ANIA',
        className="dcc_control"
                       )
        ,
dcc.Markdown('''###### Schéma logistique'''),

dcc.Dropdown(
    id='circuit',
    options=[
        {'label': 'Direct Magasin', 'value': 1},
        {'label': 'Via PTF distributeur', 'value': 2},
        {'label': 'Via PTF groupage et distributeur', 'value': 3},
        {'label': 'Via PTF groupage/dégroupage et distributeur', 'value': 4},
        {'label': 'Via PTF groupage/dégroupage', 'value': 5},
        {'label': 'Via PTF groupage', 'value': 6},
        {'label': 'Via PTF dégroupage', 'value': 7}

    ],
    value=1,
    multi=False,
        className="dcc_control"
),

        dcc.Markdown('''##### Ruptures'''),
        dcc.RadioItems(id='ruptures',
            options=[
                {'label': "Scénario 1 : Rupture d'interface", 'value': 'interface'},
                {'label': "Scénario 2 : Pas de rupture", 'value': 'no'},
                {'label': "Scénario 3 : Abus (panne ou mauvaise gestion", 'value': 'abuse'},

            ],
            value='interface'
        )
    ],className="pretty_container four columns"),



    html.Div([
    dcc.Markdown('''### Produit'''),
    dcc.Markdown(id='affichage_Tinit',style={'font-size':'170%'}),
    dcc.Slider(
        id='Tinit',
        min=-2,
        max=45,
        step=1,
        value=0
        ),
    dcc.Markdown(id='affichage_Nproduit',style={'font-size':'170%'}),
    dcc.Slider(
        id='Nproduit',
        min=1,
        max=25,
        step=1,
        value=10
        ),
    dcc.Markdown(id='affichage_poids',style={'font-size':'170%'}),
    dcc.Input(
        id='poids',
        type='number',
        value=0.25
        ),

    dcc.Markdown(id='affichage_Cp_p',style={'font-size':'170%'}),
    dcc.Input(
        id='Cp_p',
        placeholder='Heat capacity',
        type='number',
        value=3200
        ),
    dcc.Markdown(id='affichage_h',style={'font-size':'150%'}),
    html.Div
    ([html.Div([dcc.Input(
                id='h',
                type='number',
                value=10
                )])
    ]),

    html.Button('Calculer',id='calcule')],style={'font-size':'72.5%','width':'23%','display':'inline-block'}
    ),
    html.Div(

        [
        dcc.Graph(
        id='basic-interactions')
        ]
        ,style={'width':'54%','display':'inline-block'}),
    html.Button('Carte de chaleur', id='chaleur'),
html.Div(

        [
        dcc.Graph(
        id='plot_config'),
    html.Img(src=app.get_asset_url('palette.png'),style={
                                "height": "160px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            })
        ]
        ,style={'width':'100%','display':'inline-block'})
    
], id="mainContainer",
    style={"display": "flex", "flex-direction": "column",'backgroundColor':' #ebf9f2'},
)



@app.callback(
     dash.dependencies.Output('basic-interactions', 'figure'),
     [dash.dependencies.Input('calcule', 'n_clicks')],
     state=[dash.dependencies.State('Q', 'value'),\
     dash.dependencies.State('Tinit', 'value'),\
     dash.dependencies.State('Nproduit', 'value'),\
     dash.dependencies.State('poids', 'value'),\
     dash.dependencies.State('Cp_p', 'value'),\
     dash.dependencies.State('h', 'value'),\
     dash.dependencies.State('C_vent','value'),\
            dash.dependencies.State('Vfr','value'),\
            dash.dependencies.State('conduction_bool','value'),\
            dash.dependencies.State('ruptures','value'),\
            dash.dependencies.State('circuit','value')])

def update_data(calcule,Q,Tinit,Nproduit,poids,Cp_p,h,C_vent,Vfr,conduction,ruptures,circuit):

    palette0=palette(config=1,l=0.57,L=0.25,nb_l=3,nb_L=2,Q=Q,C_vent=C_vent)
    produit0=produit(Tinit=Tinit,Nproduit=Nproduit,poids=poids,Cp_p=Cp_p,Sp=0.0820325,h=h,rho=1.25,palette=palette0)
    chaine0=chaine(circuit=circuit)
    dt=30
    Ta = 0
    debut=200
    if (ruptures=='interface'):
        T,T_air=constructT_air_avec_rupture_chaine(chaine=chaine0,dt=30,lambda_rupture=0.9)
    if (ruptures=='no'):
        T,T_air=constructT_air_sans_rupture_chaine(chaine=chaine0,dt=30)
    if (ruptures=='abuse'):
        T,T_air=constructT_air_abus(dt=30)


    Tprod,T_az=calcul_profils(palette0,produit0,T_air,dt,Vfr,conduction)

    fig=plotly.tools.make_subplots(rows=1,cols=1)
    fig['layout']['legend']={'x':1,'y':1}
    fig['layout']['title']={'text':'Profil de température simulé'}
    fig['layout']['clickmode']='event+select'
    fig.append_trace({
        'x':T/3600,
        'y':T_air,
        'name':'T_air'
                },1,1)
    for k in range(1,19):
        fig.append_trace({
        'x':T/3600,
        'y':Tprod[k-1,:],
        'name':'Produit '+str(k)
        },1,1)
    fig['layout']['xaxis']={'title':'Temps (h)'}
    fig['layout']['yaxis']={'title':'Température (°C)'}
    fig.update_yaxes(range=[-1, 27])

    return fig

@app.callback(dash.dependencies.Output('affichage_longueur', component_property='children'),
    [dash.dependencies.Input(component_id='longueur', component_property='value')]
    )
def update_longeur(value):
	return "longueur: {} cm".format(value)

@app.callback(dash.dependencies.Output('plot_config',component_property='figure'),
[dash.dependencies.Input('chaleur', 'n_clicks')],
    state=[dash.dependencies.State(component_id='basic-interactions',component_property='figure')])
def update_config(chaleur,figure):

    z=np.array([figure['data'][k]['y'][0] for k in range(1,19)]).reshape(3,6).T
    x=np.array(figure['data'][0]['x'])
    time_total=len(figure['data'][1]['y'])
    colorbar=dict(
        title="Heat",
        titleside="top",
        tickmode="array",
        tickvals=[0, 4, 25],
        ticktext=["0", "8", "25"],
        ticks="outside"
    )
    text=np.array(["Produit {}".format(k) for k in range(1,19)]).reshape(3,6).T
    frames=[go.Frame(\
        data=[go.Heatmap(\
        z=np.array([figure['data'][k]['y'][value] for k in range(1,19)]).reshape(3,6).T,\
        zmid=4,colorbar=colorbar,\
        text=text)],name=str(value))
            for value in np.arange(0,time_total,step=25)]
    


    fig=go.Figure(data=go.Heatmap(z=z,zmid=4,text=text,colorbar=colorbar,),frames=frames)
    
    #fig = go.Heatmap(z,xgap=0.5,ygap=0.5,colorscale=[[0, 'rgb(0,0,255)']])
    fig['layout']['title']={'text':'Carte des produits dans la palette'}
    axis_template = dict(showgrid = False, zeroline = False,showticklabels = False,
             ticks = '' )

    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

    sliders = [
        {
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "currentvalue": {
                "font": {"size": 20},
                "suffix": " h",
                "visible": True,
                "xanchor": "right"
            },
            "steps": [
                {
                    "args": [[f.name], frame_args(0)],
                    "label": str(int(int(f.name)*30/3600)),
                    "method": "animate",
                }
                for k, f in enumerate(fig.frames)
            ],
        }
    ]
    fig.update_layout(xaxis=axis_template,yaxis=axis_template,\
                      width = 500, height =600,\
                      scene=dict(
                          zaxis=dict(range=[-0.1, 6.8], autorange=False),
                          aspectratio=dict(x=1, y=1, z=1),
                      ),\
                      updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(50)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
         ],
         sliders=sliders)
    return fig


@app.callback(dash.dependencies.Output('affichage_Tinit', component_property='children'),
    [dash.dependencies.Input(component_id='Tinit', component_property='value')]
    )

def update_Tinit(value):
	return "Température initiale: {} °C".format(value)

@app.callback(dash.dependencies.Output('affichage_Vfr', component_property='children'),
    [dash.dependencies.Input(component_id='Vfr', component_property='value')]
    )

def update_Vfr(value):
	return "Vitesse frontale: {} m/s".format(value)
    

@app.callback(dash.dependencies.Output('affichage_Q', component_property='children'),
    [dash.dependencies.Input(component_id='Q', component_property='value')]
    )

def update_Q(value):
	return "Puissance thermique par maille: {} W/m2".format(value)

@app.callback(dash.dependencies.Output('affichage_C_vent', component_property='children'),
    [dash.dependencies.Input(component_id='C_vent', component_property='value')]
    )

def update_C_vent(value):
	return "Coefficient de ventilation: {} ".format(value)

@app.callback(dash.dependencies.Output('affichage_Nproduit', component_property='children'),
    [dash.dependencies.Input(component_id='Nproduit', component_property='value')]
    )

def update_C_vent(value):
	return "Nombre de produits: {} ".format(value)

@app.callback(dash.dependencies.Output('affichage_poids', component_property='children'),
    [dash.dependencies.Input(component_id='poids', component_property='value')]
    )

def update_Cp_p(value):
	return "Poids: {} kg".format(value)

@app.callback(dash.dependencies.Output('affichage_Cp_p', component_property='children'),
    [dash.dependencies.Input(component_id='Cp_p', component_property='value')]
    )

def update_Cap(value):
	return "Capacité thermique: {} J/K".format(value)


@app.callback(dash.dependencies.Output('affichage_h', component_property='children'),
    [dash.dependencies.Input(component_id='h', component_property='value')]
    )

def update_h(value):
	return "Coefficient d'échange convectif {} W/m2/°C".format(value)
if __name__ == '__main__':
    app.run_server(debug=True)
