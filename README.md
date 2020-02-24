## Comment a été conçue cette application ?

### Interface et déploiement
* La seconde version de l'application est disponible [ici]() (l'ancienne [là]()) 
* L'interface graphique a été conçue grâce à [Dash]() et à [Plotly]() : un bon moyen de comprendre les objets utilisés est de regarder le [Dash User Guide](https://dash.plot.ly/)
* Le deploiement de l'application a été possible grâce à [Git]() et à [Heroku]()

### Modèle d'origine : modèle thermique zonal

Pour étudier les transferts d'air et de chaleur, une approche est souvent utilisée : CFD - computational fluid dynamics. Cette approche consiste à discrétiser très finement le domaine, et à résoudre un système d'équations qui décrivent les lois de la thermodynamique à respecter. Cette méthode est très précise car elle prend en compte de nombreux paramètres, mais est très coûteuse en temps et en mémoire. Des modèles simplifiés ont été développés pour obtenir des simulations plus rapidement. Un des modèle simplifié utilisé est le modèle zonal : on discrétise plus grossièrement l'équipement étudié. 

Dans cette simulation, on utilise un modèle simplifié zonal validé expérimentalement : ce modèle a été développé lors de la thèse d'Anh Thu PHAM (sur des palettes de fromage). Pour simuler les ruptures, le code a été modifié par Steven Duret de façon à y introduire un régime transitoire et calculer la conduction.

### Simulation des ruptures

Pour simuler les écoulements d'air et de chaleur dans cette palette, on doit y entrer les températures de l'air en fonction du temps. Afin de coller aux données terrain, on construit un circuit logistique (ensemble de maillons successifs) : dans cette application sont proposés les circuits les plus courants observés (Guide des bonnes pratiques logistiques). On génère ensuite les durées et températures de chaque maillon à partir des lois de distributions observées dans des études terrains (choisir entre ANIA et Morelli and Derens (2009).


| Step description  |       ANIA | Morelli and Derens (2009)|
| :------------ | :-------------: | -------------: |
|Transport      |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :  *E*()            | Time (days) : *E*() |
|Warehouse    |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) : *E*()              | Time (days) : *E*() |
|Platform        |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :  *E*()             | Time (days) : *E*() |
|Cold room        |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :   *E*()            | Time (days) : *E*() |
|Display cabinet       |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :    *E*()           | Time (days) : *E*() |
|Transport by consumer     |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :     *E*()          | Time (days) : *E*() |
|Domestic refrigerator |     Temperature (°C) : *N*(,) |     Temperature (°C) : *N*(,)|
|                |   Time (days) :    *E*()           | Time (days) :*E*()  |

Pour toute remarque/suggestion/commentaire : [julie.loisel@agroparistech.fr](julie.loisel@agroparistech.fr)
