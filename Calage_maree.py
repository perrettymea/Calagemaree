
##début du traitement

print("WARNING")
print('Avant toute chose, veuillez vérifier que vos données sont toutes au bon format.')

##Demande de l'action a effectuer:
print("Voulez vous caler vos mesures de marée :")
print("1- Avec une méthode utilisant des tirants d'air ?")
print("2-Avec une méthode par concordance avec le port de référence de votre zone de marée ?")
print("3- Avec une méthode par tirants d'air puis vérification de la valeur de calage par concordance ?")
print("Entrez le numéro de votre choix")
procedure=int(input())
##Ouverture fichier à caler et autres informations

with open("Patmo.txt", 'r') as source:
	liste_atmo=source.read().splitlines()

with open("Pmar.txt", 'r') as source:
	liste_mar=source.read().splitlines()

with open("Water_density.txt", 'r') as source:
	liste_water=source.read().splitlines()

if procedure==1 or procedure==3:
    with open("Tirant_air.txt", 'r') as source:
        liste_TA=source.read().splitlines()

##split des différentes listes, permet de les rendre plus facilement manipulables
liste_atmo_splt=[]
for i in range (0,len(liste_atmo)):
    liste_atmo_splt+=[liste_atmo[i].split()]

liste_mar_splt=[]
for i in range (0,len(liste_mar)):
    liste_mar_splt+=[liste_mar[i].split()]

liste_water_splt=[]
for i in range (0,len(liste_water)):
    liste_water_splt+=[liste_water[i].split()]

if procedure==1 or procedure==3:
    liste_TA_splt=[]
    for i in range (0,len(liste_TA)):
        liste_TA_splt+=[liste_TA[i].split()]


##ouverture fichier à remplir

destination=open("Hauteurs_maree_non_calees.txt","w")



#attribution constantes utiles
if procedure==1 or procedure==3:
    print("Veuillez rentrer la hauteur du repère du zéro hydrographique par rapport au ZH en m")
    ZH=float(input())
print("Le calcul des hauteurs non calées est en cours")

#input des valeurs utiles au calage.
g=9.81

#calcul hauteurs d'eau brutes
for i in range(0,len(liste_mar_splt)):
    #determination des valeurs à utiliser = les 3 heures ne se correspondent pas forcément entre la pression, pression atmosphérque et water density
    heure_maregraphe=liste_mar_splt[i][0]+" "+liste_mar_splt[i][1]
    #détermination Patmo
    k=0
    heure_atmospherique=liste_atmo_splt[k][0]+" "+liste_atmo_splt[k][1]
    while heure_maregraphe>heure_atmospherique and k<(len(liste_atmo_splt)-1):
        heure_atmospherique=liste_atmo_splt[k][0]+" "+liste_atmo_splt[k][1]
        k+=1
    Patmo=float(liste_atmo_splt[k][2])
    #détermination water _density
    l=0
    heure_water_density=liste_water_splt[l][0]+" "+liste_water_splt[l][1]
    while heure_maregraphe>heure_water_density and l<(len(liste_water_splt)-1):
        heure_water_density=liste_water_splt[l][0]+" "+liste_water_splt[l][1]
        l+=1
    rho=float(liste_water_splt[l][2])
    #détermination tirant air
    #pression mesuree par le maregraphe
    P=float(liste_mar_splt[i][2])
    #calcul hauteur correspondante
    h=(P-Patmo)/(rho*10*g)
    #reduction du nombre de chiffre significatif à 2 chiffres après la virgule
    #100=2chiffres après la virgule

    #ecriture dans le nouveau fichier
    #du temps
    destination.write(heure_maregraphe)

    destination.write(" ")
    #de la hauteur
    destination.write(str(h))
    #du retour à la ligne
    destination.write("\n")
destination.close()

##Calage_par_tirants-d'air
if procedure==1 or procedure==3:
    #reouverture fichier non cale
    with open("Hauteurs_maree_non_calees.txt", 'r') as source:
        liste_noncalees=source.read().splitlines()

    #Split liste_non_calées
    liste_noncalees_splt=[]
    for i in range (0,len(liste_noncalees)):
        liste_noncalees_splt+=[liste_noncalees[i].split()]

    #fonction heure_calage
    def heure_calage(index_i, index_k):
        heure_non_cale=liste_noncalees_splt[index_k][0]+" "+liste_noncalees_splt[index_k][1]
        heure_TA=liste_TA_splt[index_i][0]+" "+liste_TA_splt[index_i][1]
        #conversion pour comparaison
        heure_noncale_float=''
        for l in range(0,len(heure_non_cale)):
            if heure_non_cale[l] in ['0','1','2','3','4','5','6','7','8','9']:
                heure_noncale_float=heure_noncale_float+heure_non_cale[l]
        heure_noncale_float=float(heure_noncale_float)
        heure_TA_float=''
        for l in range(0,len(heure_TA)):
            if heure_TA[l] in ['0','1','2','3','4','5','6','7','8','9']:
                heure_TA_float=heure_TA_float+heure_TA[l]
        heure_TA_float=float(heure_TA_float)

        min_difference=((heure_TA_float-heure_noncale_float)**2)**(1/2)

        while min_difference>(60*6) and index_k<(len(liste_noncalees)-1): #on est pas dans les bonnes 5 minutes
            index_k+=1
            heure_non_cale=liste_noncalees_splt[index_k][0]+" "+liste_noncalees_splt[index_k][1]
            heure_noncale_float=''
            for l in range(0,len(heure_non_cale)):
                if heure_non_cale[l] in ['0','1','2','3','4','5','6','7','8','9']:
                    heure_noncale_float=heure_noncale_float+heure_non_cale[l]
            heure_noncale_float=float(heure_noncale_float)
            min_difference=((heure_TA_float-heure_noncale_float)**2)**(1/2)

        return index_k
    #calcul calage
    print("Le calage de vos mesures de marée par tirants d'air est en cours'")

    somme_calage=0
    k=0
    for i in range(0,len(liste_TA_splt)):
        bon_temps=heure_calage(i,k)
        k=bon_temps
        TA=float(liste_TA_splt[i][2])
        hauteur=float(liste_noncalees_splt[k][2])

        calage=hauteur-(ZH-TA)
        somme_calage+=calage

    calage=somme_calage/(len(liste_TA_splt))

    print("Le calage en mètres obtenu par les tirants d'air est le suivant")
    calage_arrondi=calage*1000
    calage_arrondi=int(calage_arrondi)
    calage_arrondi=calage_arrondi/1000

    print(calage_arrondi)

    fichier_cale=open("Hauteurs_maree_calees_par_TA.txt","w")
    #calage
    for i in range(0,len(liste_noncalees_splt)):
        if float(liste_noncalees_splt[i][2])>0:
            heure_maregraphe2=liste_noncalees_splt[i][0]+" "+liste_noncalees_splt[i][1]
            fichier_cale.write(heure_maregraphe2)
            hauteur=float(liste_noncalees_splt[i][2])
            hauteur_calee=hauteur-calage
            x = int(hauteur_calee*100)
            x = (float(x))/100
            hauteur_calee=x
            fichier_cale.write("    ")
            #de la hauteur
            fichier_cale.write(str(hauteur_calee))
            #du retour à la ligne
            fichier_cale.write("\n")

    #si pas de problème
    print("Votre fichier a bien été calé par rapport au zéro Hydrographique de votre région. Vos données sont présentes dans le .txt Hauteures_maree_calees_par_TA. ")
    print("")


    #fermeture des fichiers

    fichier_cale.close()
    #fin du calage par tirants d'air

##Concordance avec le port de référence de la zone de marée
if procedure==2 or procedure==3:
    print("Pour effectuer la concordance, des mesures sont disponibles sur le site de datashom. Il est conseillé de prendre les valeurs Validées temps différé")

    #reouverture fichier non cale
    with open("Hauteurs_maree_non_calees.txt", 'r') as source:
        liste_noncalees=source.read().splitlines()

    #Split liste_non_calées
    liste_noncalees_splt=[]
    for i in range (0,len(liste_noncalees)):
        liste_noncalees_splt+=[liste_noncalees[i].split()]

    #Ouverture fichier port de référence
    with open("Port_de_reference.txt", 'r') as source:
        liste_Port_de_reference=source.read().splitlines()

    liste_port_ref_splt=[]
    for i in range(0,len(liste_Port_de_reference)):
        liste_Port_de_reference[i]=liste_Port_de_reference[i].replace(";"," ")
    for i in range (0,len(liste_Port_de_reference)):
        liste_port_ref_splt+=[liste_Port_de_reference[i].split()]
    #modification du format de date
    print("le format de date du fichier de données du port de référence a bien été modifié")
    for i in range(0,len(liste_port_ref_splt)):
        ancienne_date=liste_port_ref_splt[i][0]
        #modification de la date
        nouvelle_date=ancienne_date[6:10]+"/"+ancienne_date[3:5]+"/"+ancienne_date[0:2]
        liste_port_ref_splt[i][0]=nouvelle_date
    #filtre valeures négatives
    hauteur_concordance_splt=liste_noncalees_splt
    negatif=[]
    for i in range(0,len(hauteur_concordance_splt)):
        if float(hauteur_concordance_splt[i][2])<0:
            negatif+=[hauteur_concordance_splt[i]]
    for i in range(0,len(negatif)):
        hauteur_concordance_splt.remove(negatif[i])
    #filtres basses mers: une basse mer est présente toutes les 144 mesures pour une période d'acquisition de 5min (à généraliser)


    #détermination BM chez marégraphe
    print("Quelle est la période d'acquisition de votre marégraphe (en min)?")
    periode_acquisition_maregraphe=int(input())
    periode_BM_mar=int(12.4*60/periode_acquisition_maregraphe)
    nombres_de_BM=int(len(hauteur_concordance_splt)/periode_BM_mar)

    a_garderX=[]
    for i in range(0,nombres_de_BM):
        debut=i*periode_BM_mar
        fin=(i+1)*periode_BM_mar
        mini = float(hauteur_concordance_splt[debut][2])
        indice_mini=debut
        k=debut
        while k<fin:
            if float(hauteur_concordance_splt[k][2]) <= mini:
                mini = float(hauteur_concordance_splt[k][2])
                indice_mini=k
            k+=1

        a_garderX+=[hauteur_concordance_splt[indice_mini]]
    hauteur_concordance_splt=a_garderX
    #détermination BM port de référence
    print("Quelle est la période des mesures réalisées dans le port de référence (en min)?")
    periode_acquisition_ref=int(input())
    periode_BM_ref=int(12.4*60/periode_acquisition_ref)
    a_gardery=[]
    for i in range(0,nombres_de_BM):
        debut=i*periode_BM_ref
        fin=(i+1)*periode_BM_ref
        mini = float(liste_port_ref_splt[debut][2])
        indice_mini=debut
        k=debut
        while k<fin:
            if float(liste_port_ref_splt[k][2]) <= mini:
                mini = float(liste_port_ref_splt[k][2])
                indice_mini=k
            k+=1

        a_gardery+=[liste_port_ref_splt[indice_mini]]
    liste_port_ref_splt=a_gardery



    #Construction du jeu de données
    print("La construction du jeu de données pour la concordance est en cours")
    X=[]
    y=[]
    verification=open("Valeurs_x_y.txt","w")
    k=0
    for i in range(0,len(hauteur_concordance_splt)):
        #determination des valeurs à utiliser = les 2 heures ne se correspondent pas forcément entre les hauteurs du port de référence et les hauteurs du port à caler
        X+=[float(hauteur_concordance_splt[i][2])]
        y+=[float(liste_port_ref_splt[i][2])]
        verification.write(hauteur_concordance_splt[i][2])

        verification.write(" ")
        #de la hauteur
        verification.write(liste_port_ref_splt[i][2])
        #du retour à la ligne
        verification.write("\n")
    verification.close()



    #Régression linéaire
    import numpy as np

    import matplotlib.pyplot as plt
    from scipy import stats
    #créer un objet reg lin
    X=np.asarray(X)
    y=np.asarray(y)

    print("La régression linéaire est en cours")
    from scipy import stats
    #linregress() renvoie plusieurs variables de retour. On s'interessera
    # particulierement au slope et intercept
    slope, intercept, r_value, p_value, std_err = stats.linregress(y,X)
    print("slope: %f    intercept: %f" % (slope, intercept))
    print("Le coefficient R^2 vaut :")
    print(r_value)
    print("La valeur de calage de notre marégraphe en mètres determinée par concordance vaut :")
    calage_arrondi=intercept*1000
    calage_arrondi=int(calage_arrondi)
    calage_arrondi=calage_arrondi/1000

    print(calage_arrondi)
    print("Fermer la fenêtre du graphe pour continuer le traitement")

    plt.plot(y, X, 'o', label='mesures de marée')
    plt.xlabel("Hauteurs mesurées dans le port de référence")
    plt.ylabel("Hauteurs mesurées par le marégraphe")
    plt.plot(y, intercept + slope*y, 'r', label='régression linéaire')
    plt.legend()
    plt.show()

if procedure==2:
    #Détermination valeur du calage par concordance
    calage=intercept

    #Calage par concordance
    fichier_cale2=open("Hauteurs_maree_calees_par_concordance.txt","w")
    #calage
    print("Le calage de vos mesures de marée par concordance est en cours")
    for i in range(0,len(liste_noncalees_splt)):
        heure_maregraphe2=liste_noncalees_splt[i][0]+" "+liste_noncalees_splt[i][1]
        fichier_cale2.write(heure_maregraphe2)
        hauteur=float(liste_noncalees_splt[i][2])
        hauteur_calee=hauteur-calage
        x = int(hauteur_calee*100)
        x = (float(x))/100
        hauteur_calee=x
        fichier_cale2.write("    ")
        #de la hauteur
        fichier_cale2.write(str(hauteur_calee))
        #du retour à la ligne
        fichier_cale2.write("\n")

    #si pas de problème
    print("Votre fichier a bien été calé par rapport au zéro Hydrographique de votre région.    Vos données sont présentes dans le .txt Hauteures_maree_calees_par_concordance. ")
    print("")


    #fermeture des fichiers

    fichier_cale2.close()
##pause pour que la fenêtre ne se ferme pas
print("Taper sur Entrée si vous voulez fermer la fenêtre")
input()