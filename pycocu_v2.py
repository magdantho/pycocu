import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math
import datetime
from mpl_toolkits import mplot3d
import plotly.express as px

carnets = pd.read_csv("pyth_carnets.csv", sep=";",
                      decimal=",", index_col=0, header='infer')
carnets.drop(["Remarque", 'X', 'Y', 'Z', 'Xmoy', 'Ymoy', 'Zmoy'],
             axis=1, inplace=True)

carnets["Datation"].fillna(0,inplace=True)
dates = carnets[carnets["Datation"]!=0]

color_dict_ua = dict({'UA 1a': 'sienna',
                      'UA 1b': 'darkorange',
                      'UA 2': '#FFF82C',
                      'UA 3': 'limegreen',
                      'UA 4a': 'salmon',
                      'UA 4b': 'dodgerblue',
                      'UA 4c': 'skyblue',
                      'UA 5a': 'sandybrown',
                      'UA 5b': 'hotpink',
                      'UA ?': 'gainsboro'})

color_dict_nature = dict({'Lithique': 'mediumblue',
                          'Galet': 'dodgerblue',
                          'Plaquette': 'skyblue',
                          'Gres': 'cyan',
                          'Calcaire': 'grey',
                          'Faune': 'lightcoral',
                          'Indos': 'limegreen',
                          'Esquille': 'gold',
                          'Coquille': 'deeppink',
                          'Ocre/Oxydes/Colorants': 'darkred',
                          'Charbon': 'black',
                          'Débris': 'gainsboro',
                          'indet': 'gainsboro',
                          })


def points_proj(x, ep, t):
    if t == 's':
        df = carnets.loc[(carnets["Xabs"] >= x) & (carnets["Xabs"] < x+ep)]

    elif t == 'f':
        df = carnets.loc[(carnets["Yabs"] >= x) & (carnets["Yabs"] < x+ep)]

    elif t == 'p':
        df = carnets.loc[(carnets["Zabs"] >= x) & (carnets["Zabs"] < x+ep)]

    return df
    
    
def title_fig(x, ep, t):
    if t == 's':
        title = "Coupe sagittale " + str(x) + " ≤ x < " + str(x + ep)
    elif t == 'f':
        title = "Coupe frontale " + str(x) + " ≤ y < " + str(x + ep)
    elif t == 'p':
        title = "Vue planaire " + str(x) + " ≤ z < " + str(x + ep)
    return title
    
def nom_fig(x, ep, t):
    if t == 's':
        nom = "Coupe sagittale_" + str(x) + "-" + str(x + ep)
    elif t == 'f':
        nom = "Coupe frontale_" + str(x) + "-" + str(x + ep)
    elif t == 'p':
        nom = "Vue plan_" + str(x) + "-" + str(x + ep)
    return nom
    
    
def type_proj():
    tp = input("Type de coupe à afficher : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire : ")
    
    if tp.lower() in ['s', 'f', 'p']:
        return tp.lower()
    
    else:
        return "Valeur incorrecte, recommencez !"
        
        
def type_color():
    tc = input("Choisir entre 'ua' (colorer les points selon leur UA) ou 'nat' (selon leur nature) : ")
    if tc.lower() == 'ua':
        cat = ("UA", color_dict_ua)
        return cat
    elif tc.lower() == 'nat':
        cat = ("Nature", color_dict_nature)
        return cat
    else:
        return "Valeur incorrecte, recommencez !"
        
        
def coloration(tc):
    if tc.lower() == 'ua':
        cat = ("UA", color_dict_ua)
        return cat
    elif tc.lower() == 'nat':
        cat = ("Nature", color_dict_nature)
        return cat
    else:
        pass
        
        
def sauvegarde_fig(x, ep, t, f):
    format_sortie = f.lower()
    date = datetime.datetime.now()
    figname = 'figures/'+nom_fig(x, ep, t)+'_'+str(date.year)+str(date.month)+str(date.day)+'_'+str(date.hour)+'h'+str(date.minute)+'.'+format_sortie
    plt.savefig(figname)
    return "La figure a été enregistrée sous le nom : " + figname
    
    
def tabl_dates():
    carnets["Datation"].fillna(0,inplace=True)
    dates = carnets[carnets["Datation"]!=0]
    return dates.sort_values(by='Datation')
    
    
def plan_proj(x1, ep, t):
    """
    Cette fonction affiche une vue planaire de la projection donnée en paramètres.
    x1 = valeur à partir de laquelle commence la projection
    ep = épaisseur de la projection (en cm)
    t = type de projection : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire 
    """
    plt.rcParams.update(plt.rcParamsDefault)
    # plt.figure(figsize=(6.693,5.12)) #format en inch (17 x 13 cm)
    dfp = points_proj(x1, ep, t)
    plt.title("Position de la coupe")

    #plt.scatter("Xabs","Yabs",s=1, c='navy', marker="o",data=dfp)

    sns.scatterplot(x="Xabs",
                    y="Yabs",
                    s=3,
                    marker='o',
                    color='navy',
                    data=dfp,
                    edgecolor='dimgrey',
                    linewidth = 0.3
                    )

    axes = plt.gca()
    axes.set_xticks(range(0, 800, 100), minor=False)
    axes.set_xticks(range(0, 800, 50), minor=True)
    axes.xaxis.set_ticklabels(['G', 'H', 'I', 'J', 'K', 'L', 'M'],
                              minor=True, rotation=0, style='normal')
    axes.xaxis.set_tick_params(which='major',
                               length=5,
                               width=1,
                               labelcolor='k')
    axes.xaxis.set_tick_params(which='minor',
                               length=5,
                               color='w',
                               labelsize=12,
                               labelcolor='dimgray')

    axes.set_yticks(range(0, 800, 100), minor=False)
    axes.set_yticks(range(0, 800, 50), minor=True)
    axes.yaxis.set_ticklabels(['26', '25', '24', '23', '22', '21', '20', '19'],
                              minor=True, rotation=0, style='normal')
    axes.yaxis.set_tick_params(which='major',
                               length=5,
                               width=1,
                               labelcolor='k')
    axes.yaxis.set_tick_params(which='minor',
                               length=8,
                               color='w',
                               labelsize=12,
                               labelcolor='dimgray')

    plt.axis('equal')
    plt.xlabel("X (cm)")
    plt.ylabel("Y (cm)")
    plt.grid(color='silver',
             linestyle='--',
             linewidth=0.75)
             


def projection(x1,ep,t,color):
    """ 
    x1 = valeur à partir de laquelle commence la projection
    ep = épaisseur de la projection (en cm)
    t = type de projection : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire
    colortype = type de coloration : 'ua' (selon leur UA) ou 'nat' (selon leur nature)
    f = format de sortie ('eps', 'jpg', 'pdf', 'png', 'ps', 'raw', 'svg', 'svgz', 'tif', 'tiff')
    """
    plt.rcParams.update(plt.rcParamsDefault)
    #plt.figure(figsize=(6.693,4.855)) #format en inch (17 x 12.332 cm)
    
    df = points_proj(x1,ep,t)
    titlefig = title_fig(x1,ep,t)
        
    plt.title(titlefig)
    colortype = coloration(color)
    plt.grid(color='silver',
             linestyle='--',
             linewidth=0.75)
    axes = plt.gca()
    axes.set_xticks(range(0,800,50), minor = True)
    axes.set_xticks(range(0,800,100), minor = False)
    
    if t =='s': 
        print("La projection souhaitée, d'une épaisseur de", ep, "cm, se fera entre x=", x1, "et x=", (x1 + ep))
        sns.scatterplot(x="Yabs", 
                        y="Zabs", 
                        s=15,
                        marker='o',
                        hue=colortype[0],
                        palette=colortype[1],
                        data=df.sort_values(by=colortype[0]),
                        edgecolor = "dimgrey",
                        linewidth = 0.40)
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)")
        axes.set_yticks(range(-600,0,100), minor = False)
        axes.set_yticks(range(-650,-50,50), minor = True)
        axes.xaxis.set_ticklabels(['26','25','24','23','22','21','20','19'],
                                  minor = True, rotation = 0, style = 'normal')
        axes.xaxis.set_tick_params(which = 'major', 
                                   length = 5, 
                                   width = 1,
                                   labelcolor = 'k')
        axes.xaxis.set_tick_params(which = 'minor',
                                   length = 5,
                                   color = 'w', 
                                   labelsize = 12, 
                                   labelcolor = 'dimgray')

    elif t == "f":
        print("La projection souhaitée, d'une épaisseur de", ep, "cm, se fera entre y=", x1, "et y=", (x1 + ep))
        sns.scatterplot(x="Xabs", 
                        y="Zabs", 
                        s=15,
                        marker='o',
                        hue=colortype[0],
                        palette=colortype[1],
                        data=df.sort_values(by=colortype[0]),
                        edgecolor = "dimgrey",
                        linewidth = 0.40)
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)")
        axes.set_yticks(range(-600,0,100), minor = False)
        axes.set_yticks(range(-650,-50,50), minor = True)        
        axes.xaxis.set_ticklabels(['G','H','I','J','K','L','M'], 
                                  minor = True, rotation = 0, style = 'normal')
        axes.xaxis.set_tick_params(which = 'major', 
                                   length = 5, 
                                   width = 1,
                                   labelcolor = 'k')
        axes.xaxis.set_tick_params(which = 'minor',
                                   length = 5,
                                   color = 'w', 
                                   labelsize = 12, 
                                   labelcolor = 'dimgray')

    elif t=='p':
        print("La plan souhaité, d'une épaisseur de", ep, "cm, se fera entre z=", x1, "et z=", (x1 + ep))
        sns.scatterplot(x="Xabs", 
                        y="Yabs", 
                        s=15,
                        marker='o',
                        hue=colortype[0],
                        palette=colortype[1],
                        data=df.sort_values(by=colortype[0]),
                        edgecolor = "dimgrey",
                        linewidth = 0.40)
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")

        axes.xaxis.set_ticklabels(['G','H','I','J','K','L','M'], 
                                  minor = True, rotation = 0, style = 'normal')
        axes.xaxis.set_tick_params(which = 'major', 
                                   length = 5, 
                                   width = 1,
                                   labelcolor = 'k')
        axes.xaxis.set_tick_params(which = 'minor',
                                   length = 5,
                                   color = 'w', 
                                   labelsize = 12, 
                                   labelcolor = 'dimgray')
        axes.set_yticks(range(0,800,100), minor = False)
        axes.set_yticks(range(0,800,50), minor = True)
        axes.yaxis.set_ticklabels(['26','25','24','23','22','21','20','19'], 
                                  minor = True, rotation = 0, style = 'normal')
        axes.yaxis.set_tick_params(which = 'major', 
                                   length = 5, 
                                   width = 1,
                                   labelcolor = 'k')
        axes.yaxis.set_tick_params(which = 'minor',
                                   length = 8,
                                   color = 'w', 
                                   labelsize = 12, 
                                   labelcolor = 'dimgray')        
        
    else:
        pass
    
    plt.axis('equal')
    
    plt.legend(loc="best",
               fontsize='small', 
               facecolor='white', 
               framealpha=1, 
               edgecolor='0.9', 
               shadow=True,
               labelspacing=0.3)
    
    #plt.savefig(nomfig+format_sortie)
    #print("La figure a été enregistrée sous le nom : ",nomfig+format_sortie)
    
    

def dates_proj(x1,ep,t):
    """ 
    Projection des objets datés.
    x1 = valeur à partir de laquelle commence la projection
    ep = épaisseur de la projection (en cm)
    t = type de projection : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire
    """
    dates = tabl_dates()
    if t =='s':
        df = dates.loc[(dates["Xabs"]>=x1) & (dates["Xabs"]<x1+ep)]

    elif t =='f':
        df = dates.loc[(dates["Yabs"]>=x1) & (dates["Yabs"]<x1+ep)]

    elif t =='p':
        df = dates.loc[(dates["Zabs"]>=x1) & (dates["Zabs"]<x1+ep)]

    else:
        pass
    
    if t =='s': 
        sns.scatterplot(x="Yabs",y="Zabs", 
                        s=100,
                        marker='*',
                        color = 'red',
                        data=df.sort_values(by="Date_bp"),
                        edgecolor = "darkred",
                        linewidth = 0.40, 
                        label="Datation")
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)")  
            
    elif t =='f': 
        sns.scatterplot(x="Xabs",y="Zabs", 
                        s=100,
                        marker='*',
                        color = 'red',
                        data=df.sort_values(by="Date_bp"),
                        edgecolor = "darkred",
                        linewidth = 0.40, 
                        label="Datation")
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)")    
            
    elif t =='p': 
        sns.scatterplot(x="Xabs",y="Yabs", 
                        s=70,
                        marker='*',
                        color = 'red',
                        data=df.sort_values(by="Date_bp"),
                        edgecolor = "darkred",
                        linewidth = 0.40, 
                        label="Datation")
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")



def proj_totale(x1, ep, t, color):
    fig = plt.figure(figsize=(7.677, 10.852))  # format en inch
    dates = tabl_dates()
    plt.subplot(2, 1, 1)
    projection(x1, ep, t, color)
    dates_proj(x1, ep, t)
    plt.legend(loc='best',
               fontsize='small',
               facecolor='white',
               framealpha=1,
               edgecolor='0.9',
               shadow=True,
               labelspacing=0.3)
    if t == 's':
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)")
        df = dates.loc[(dates["Xabs"] >= x1) & (dates["Xabs"] < x1+ep)]
    elif t == "f":
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)")
        df = dates.loc[(dates["Yabs"] >= x1) & (dates["Yabs"] < x1+ep)]
    elif t == 'p':
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")

    plt.subplot(2, 1, 2)
    plan_proj(x1, ep, t)
    sns.scatterplot(x="Xabs", y="Yabs",
                    s=70,
                    marker='*',
                    color='red',
                    data=df,
                    edgecolor="darkred",
                    linewidth=0.40,
                   label="Datation")

    # plt.legend()



def proj_totale(x1, ep, t, color):
    fig = plt.figure(figsize=(7.677, 10.852))  # format en inch
    dates = tabl_dates()
    plt.subplot(2, 1, 1)
    projection(x1, ep, t, color)
    dates_proj(x1, ep, t)
    plt.legend(loc='best',
               fontsize='small',
               facecolor='white',
               framealpha=1,
               edgecolor='0.9',
               shadow=True,
               labelspacing=0.3)
    if t == 's':
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)")
        df = dates.loc[(dates["Xabs"] >= x1) & (dates["Xabs"] < x1+ep)]
    elif t == "f":
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)")
        df = dates.loc[(dates["Yabs"] >= x1) & (dates["Yabs"] < x1+ep)]
    elif t == 'p':
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")

    plt.subplot(2, 1, 2)
    plan_proj(x1, ep, t)
    sns.scatterplot(x="Xabs", y="Yabs",
                    s=70,
                    marker='*',
                    color='red',
                    data=df,
                    edgecolor="darkred",
                    linewidth=0.40,
                   label="Datation")

    # plt.legend()


def proj_3d():
    """ 
    x1 = valeur à partir de laquelle commence la projection
    ep = épaisseur de la projection (en cm)
    t = type de projection : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire
    colortype = type de coloration : 'ua' (selon leur UA) ou 'nat' (selon leur nature)    
    """
    df = carnets[["Xabs", "Yabs", "Zabs", "UA","Nature", "Couche"]].sort_values(by="UA")

    fig = px.scatter_3d(df,
                        x='Xabs',
                        y='Yabs',
                        z='Zabs',
                        hover_data=["Nature", "Couche", df.index],
                        color='UA',
                        color_discrete_map=color_dict_ua,
                        width=900, height=900
                        )
    fig.update_traces(marker=dict(size=1,
                                  line=dict(width=0,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.update_layout(title="Figure interractive",
                      coloraxis_showscale=False,
                      showlegend=True,
                      template='plotly_dark',
                      paper_bgcolor='gray',
                      plot_bgcolor='white',
                      legend={'itemsizing': 'constant',
                              'traceorder': 'normal'}
                      )

    fig.update_xaxes(showline=True,
                     linewidth=2,
                     linecolor='white',
                     gridcolor="grey",
                     zerolinecolor="grey"
                     )
    fig.update_yaxes(showline=True,
                     linewidth=2,
                     linecolor='white',
                     gridcolor="grey",
                     zerolinecolor="grey"
                     )

    fig.show()



def ou_es_tu(ID, ep, t, color):
    """
    Cette fonction permet d'afficher une projection autour de 
    l'objet dont l'ID est donné en paramètre.
    ID : identifiant de l'objet (carré-numéro) entre guillemet double "". Exemple : "K23-24"
    ep = épaisseur de la projection (en cm)
    t = type de projection : 's' pour sagittale, 'f' pour frontale et 'p' pour planaire
    color = type de coloration : 'ua' (selon leur UA) ou 'nat' (selon leur nature)
    """
    # Extraction des coordonnées
    df = pd.DataFrame(carnets.loc[ID]).T
    x_id = float(carnets.loc[ID, ["Xabs"]])
    y_id = float(carnets.loc[ID, ["Yabs"]])
    z_id = float(carnets.loc[ID, ["Zabs"]])
    print(carnets.loc[ID, ["Carre", "Numero", "Couche", "Nature",
                           "Annee", "Xabs", "Yabs", "Zabs", "UA",
                           "Datation"]], end='\n\n')
    fig = plt.figure(figsize=(7.677, 10.852))  # format en inch

    # Condition selon type de coupe
    if t == 's':
        plt.subplot(2, 1, 1)
        projection(x_id-ep/2, ep, 's', color)
        sns.scatterplot(x="Yabs", y="Zabs",
                        s=100,
                        marker='X',
                        color='m',
                        data=df,
                        edgecolor="black",
                        linewidth=0.70,
                        label=ID)
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)") 
        plt.subplot(2, 1, 2)
        plan_proj(x_id-ep/2, ep, 's')
        sns.scatterplot(x="Xabs", y="Yabs",
                        s=100,
                        marker='X',
                        color='m',
                        data=df,
                        edgecolor="black",
                        linewidth=0.70,
                        label=ID)
        plt.xlabel("Y (cm)")
        plt.ylabel("Z (cm)") 
        
    if t == 'f':
        plt.subplot(2, 1, 1)
        projection(y_id-ep/2, ep, 'f', color)
        sns.scatterplot(x="Xabs", y="Zabs",
                        s=100,
                        marker='X',
                        color='m',
                        data=df,
                        edgecolor="black",
                        linewidth=0.70,
                        label=ID)
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)") 
        plt.subplot(2, 1, 2)
        plan_proj(y_id-ep/2, ep, 'f')
        sns.scatterplot(x="Xabs", y="Yabs",
                        s=100,
                        marker='X',
                        color='m',
                        data=df,
                        edgecolor="black",
                        linewidth=0.70,
                        label=ID)
        plt.xlabel("X (cm)")
        plt.ylabel("Z (cm)") 
    if t == 'p':
        plt.subplot(2, 1, 1)
        projection(z_id-ep/2, ep, 'p', color)
        sns.scatterplot(x="Xabs", y="Yabs",
                        s=100,
                        marker='X',
                        color='m',
                        data=df,
                        edgecolor="black",
                        linewidth=0.70,
                        label=ID)
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)") 

    plt.show()



