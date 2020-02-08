# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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
app.config['suppress_callback_exceptions']=True
app.layout = html.Div([
    html.Div([
        #############Coté gauche###########
    dcc.Markdown('''### Construction de la palette'''),
    dcc.Markdown('''Première version d'une application implémentée en Python par Julie Loisel
    utilisant le modèle codé en Matlab par Denis Flick (AgroParisTech)
    et repris par Steven Duret(IRSTEA).
    '''),
    dcc.Markdown(id='affichage_C_vent',style={'font-size':'170%'}),
    dcc.Slider(
        id='C_vent',
        min=0.,
        max=3,
        step=0.01,
        value=1.
        ),

    dcc.Markdown(id='affichage_Vfr',style={'font-size':'170%'}),
    dcc.Slider(
        id='Vfr',
        min=0,
        max=3,
        step=0.1,
        value=0.31),

    dcc.Markdown(id='affichage_Q',style={'font-size':'170%'}),

    dcc.Slider(
        id='Q',
        min=0.,
        max=1.,
        step=0.02,
        value=0.04
        ),
dcc.Markdown('''##### Calculer la conduction'''),
        dcc.RadioItems(id='conduction_bool',
            options=[
                {'label': 'Oui', 'value': 1},
                {'label': 'Non', 'value': 0},

            ],
            value=1
        ),
        dcc.Markdown('''##### Ruptures'''),
        dcc.RadioItems(id='ruptures',
            options=[
                {'label': 'Aléatoires', 'value': 'alea'},
                {'label': 'Scénario 1: 3 ruptures', 'value': '1'},
                {'label': 'Scénario 2: 4 ruptures', 'value': '2'},

            ],
            value='alea'
        )
    ],style={'font-size':'72.5%','width':'23%','display':'inline-block'}),
##### RUPTURES #####


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
        id='plot_config')
        ]
        ,style={'width':'54%','display':'inline-block'}),
    html.Div(

        [
        dcc.Graph(
        id='basic-interactions')
        ]
        ,style={'width':'100%','display':'inline-block'})
    
],style={'backgroundColor':'#ecf2f9'})



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
            dash.dependencies.State('ruptures','value')])

def update_data(calcule,Q,Tinit,Nproduit,poids,Cp_p,h,C_vent,Vfr,conduction,ruptures):

    palette0=palette(config=1,l=0.57,L=0.25,nb_l=3,nb_L=2,Q=Q,C_vent=C_vent)
    produit0=produit(Tinit=Tinit,Nproduit=Nproduit,poids=poids,Cp_p=Cp_p,Sp=0.0820325,h=h,rho=1.25,palette=palette0)
    dt=30
    Ta = 0
    debut=200
    if (ruptures=='alea'):
        nb_ruptures=random.randint(2,6)
        durees=[random.randint(20,50) for i in range(nb_ruptures)]
        pauses=[random.randint(20,1000) for i in range(nb_ruptures)]
        temperatures=[random.randint(15,30) for i in range(nb_ruptures)]
    if (ruptures=='1'):
        nb_ruptures = 3
        durees = [50,60,70]
        pauses = [140,110,250]
        temperatures = [15,25,20]
    if (ruptures=='2'):
        nb_ruptures = 4
        durees = [60,50,100,100]
        pauses = [110,150,1200,170]
        temperatures = [25,15,20,20]
    T,T_air=construct_T_air_bis(dt,Ta,debut,durees,pauses,temperatures)

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

    return fig

@app.callback(dash.dependencies.Output('affichage_longueur', component_property='children'),
    [dash.dependencies.Input(component_id='longueur', component_property='value')]
    )
def update_longeur(value):
	return "longueur: {} cm".format(value)

@app.callback(dash.dependencies.Output('plot_config',component_property='figure'),
    [dash.dependencies.Input(component_id='basic-interactions',component_property='figure')])
def update_config(figure):

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
                      width = 500, height = 500,\
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
