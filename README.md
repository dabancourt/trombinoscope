# trombinoscope
TP python git


comment avoir un clé d'accès au projet ?
http://jeedom.sigalou-domotique.fr/github-support-for-password-authentication-was-removed-on-august-13-2021

-----------------------------------
préparer le projet :

git clone https://github.com/dabancourt/trombinoscope

cd trombinoscope/
-----------------------------------
modifier le projet :

git add nom-du-fichier-sur-lequel-on-travaille.py
git commit
git push

git pull
-----------------------------------
parfois, 2 dev ont travaillé sur le même fichier,
- le 1er peut faire commit/push sans problème
- le 2eme peut faire commit/ mais pas push
  il doit faire "pull" (pour récupérer le travail du 1er dev)
  et parfois fusionner les fichiers communs :

git config pull.rebase false
-----------------------------------

https://www.letecode.com/github-comment-generer-un-jeton-d-acces-personnel-pour-l-authentification


test

test2

test3

Projet avec des objets :

les objets uniquement pour "éviter" la notion de global
car pas d'héritage
et une seule instance par Objet (ce qui limite son utilité !)

- IHMtrombi

crop=[] # chaque élément contient 4 valeurs... x0,y0,x1,y1
listeNomPrenom=[]   # des tuples (nom, prenom)
listeImages=[]
listeSoustitres=[]

nomImageGauche=""
imageGauche=None
idImageGauche = 0
ligne=0
sousTitre=""
#taille des images dans fichier word...
width, height = 0,0
widthGauche, heightGauche = 0,0
numPoint=0
Largeur=307
Hauteur=348
vx0,vy0,vx1,vy1=0,0,0,0 #CROP des photos ! valeur sur l'image reelle (pour couper)
x0,y0,x1,y1=0,0,100,100 #CROP des photos ! valeur du clic (écran en pixel)


- BackOffice (système et dossiers)
listeImage = []
listeNomPrenom = []    # tableau de tuple ("dupond","toto")...  il faut vérifier nb de nom = nb d'images...
dossierImages = ""
dossierZip = ""
nbImage = 0
nbImageMax = 0
dossierWord = ""
source="trombi-6x3.docx"
#taille des images dans fichier word...
Largeur=307
Hauteur=348
dossier=""  #premier dossier d'images...

autre solution :
- classe ImageTrombi
crop
nomPrenom
libelle
numero

et on travaille uniquement sur une liste : ImageTrombi[]



