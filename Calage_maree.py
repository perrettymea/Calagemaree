print("WARNING")
print("Avant toute chose, veuillez vérifier que vos données sont toutes au même format que les fichiers en exemple. Merci")
##Demande de l'action a effectuer:
print("Voulez vous caler vos mesures de marée :")
print("1- Avec une méthode utilisant des tirants d'air ?")
print("2-Avec une méthode par concordance avec le port de référence de votre zone de marée ?")
print("3- Avec une méthode par tirants d'air puis vérification de la valeur de calage par concordance ?")
print("Entrez le numéro de votre choix")
procedure=int(input())
##Ouverture fichier à caler

with open("Patmo.txt", 'r') as source:
	liste_atmo=source.read().splitlines()

with open("Pmar.txt", 'r') as source:
	liste_mar=source.read().splitlines()

with open("Water_density.txt", 'r') as source:
	liste_water=source.read().splitlines()

with open("Tirant_air.txt", 'r') as source:
	liste_TA=source.read().splitlines()

##split des différentes listes
liste_atmo_splt=[]
for i in range (0,len(liste_atmo)):
    liste_atmo_splt+=[liste_atmo[i].split()]

liste_mar_splt=[]
for i in range (0,len(liste_mar)):
    liste_mar_splt+=[liste_mar[i].split()]

liste_water_splt=[]
for i in range (0,len(liste_water)):
    liste_water_splt+=[liste_water[i].split()]

liste_TA_splt=[]
for i in range (0,len(liste_TA)):
    liste_TA_splt+=[liste_TA[i].split()]


##ouverture fichier à remplir

destination=open("Hauteurs_maree_non_calees.txt","w")

fichier_cale=open("Hauteurs_maree_calees.txt","w")

#attribution constantes utiles
print("Veuillez rentrer la hauteur du repère du zéro hydrographique par rapport au ZH")
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


##reouverture fichier non cale
with open("Hauteurs_maree_non_calees.txt", 'r') as source:
	liste_noncalees=source.read().splitlines()

##Split liste_non_calées
liste_noncalees_splt=[]
for i in range (0,len(liste_noncalees)):
    liste_noncalees_splt+=[liste_noncalees[i].split()]

##fonction heure_calage
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
##calcul calage
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

print("Le calage obtenu par les tirants d'air est le suivant")
print(calage)

##calage
for i in range(0,len(liste_noncalees_splt)):
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

##si pas de problème
print("Votre fichier a bien été calé par rapport au zéro Hydrographique de votre région. Vos données sont présentes dans le .txt Hauteures_maree_calees. ")
print("")


##fermeture des fichiers

fichier_cale.close()

##Ouverture fichier port de référence
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


##find_the nearest hour = permet de trouver la valeur la plus proche du port de référence correspondant à nos hauteurs non calees
def find_nearest(index_i,index_k):
    heure_non_cale=liste_noncalees_splt[index_i][0]+" "+liste_noncalees_splt[index_i][1]
    heure_port_de_ref=liste_port_ref_splt[index_k][0]+" "+liste_port_ref_splt[index_k][1]
    #conversion pour comparaison
    heure_noncale_float=''
    for l in range(0,len(heure_non_cale)):
        if heure_non_cale[l] in ['0','1','2','3','4','5','6','7','8','9']:
            heure_noncale_float=heure_noncale_float+heure_non_cale[l]
    heure_noncale_float=float(heure_noncale_float)
    heure_port_float=''
    for l in range(0,len(heure_port_de_ref)):
        if heure_port_de_ref[l] in ['0','1','2','3','4','5','6','7','8','9']:
            heure_port_float=heure_port_float+heure_port_de_ref[l]
    heure_port_float=float(heure_port_float)
    min_difference=((heure_port_float-heure_noncale_float)**2)**(1/2)
    while min_difference>(60) and index_k<(len(liste_port_ref_splt)-1): #on est pas dans la bonne minute
        index_k+=1
        heure_port_de_ref=liste_port_ref_splt[index_k][0]+" "+liste_port_ref_splt[index_k][1]
        heure_port_float=''
        for l in range(0,len(heure_port_de_ref)):
            if heure_port_de_ref[l] in ['0','1','2','3','4','5','6','7','8','9']:
                heure_port_float=heure_port_float+heure_port_de_ref[l]
        heure_port_float=float(heure_port_float)
        min_difference=((heure_port_float-heure_noncale_float)**2)**(1/2)
    return index_k
##Construction du jeu de données
print("La construction du jeu de données pour la concordance est en cours")
X=[]
y=[]
verification=open("Valeurs_x_y.txt","w")
k=0
for i in range(0,len(liste_noncalees_splt)):
    #determination des valeurs à utiliser = les 2 heures ne se correspondent pas forcément entre les hauteurs du port de référence et les hauteurs du port à caler
    bonne_heure=find_nearest(i,k)
    k=bonne_heure
    X+=[float(liste_noncalees_splt[i][2])]
    y+=[float(liste_port_ref_splt[bonne_heure][2])]
    verification.write(liste_noncalees_splt[i][2])

    verification.write(" ")
    #de la hauteur
    verification.write(liste_port_ref_splt[bonne_heure][2])
    #du retour à la ligne
    verification.write("\n")
verification.close()



##nettoyage des valeurs négatives (cas impossibles dus à la non immersion du capteur)
print("Les valeurs de hauteurs négatives sont enlevées car ne représentent pas de mesure de marée")

Xliste_a_enlever=[]
Yliste_a_enlever=[]
#determination des valeurs à enlever
for k in range(0,len(X)):
    if X[k]<0:
        Xliste_a_enlever+=[X[k]]
        Yliste_a_enlever+=[y[k]]
#suppresion de ces valeurs
for l in range(0,len(Xliste_a_enlever)):
    X.remove(Xliste_a_enlever[l])
    y.remove(Yliste_a_enlever[l])

##Régression linéaire
import numpy as np
import pandas as pd
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
print("La valeur de calage de notre marégraphe determiné par concordance vaut :")
print(intercept)

plt.plot(y, X, 'o', label='mesures de marée')
plt.plot(y, intercept + slope*y, 'r', label='régression linéaire')
plt.legend()
plt.show()

##Détermination valeur du calage par concordance
calage=intercept

##Calage par concordance
fichier_cale2=open("Hauteurs_maree_calees_par_concordance.txt","w")
##calage
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

##si pas de problème
print("Votre fichier a bien été calé par rapport au zéro Hydrographique de votre région. Vos données sont présentes dans le .txt Hauteures_maree_calees. ")
print("")


##fermeture des fichiers

fichier_cale2.close()
##pause pour que la fenêtre ne se ferme pas
print("Taper sur Entrée si vous voulez fermer la fenêtre")
input()