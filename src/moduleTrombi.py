
# Pour créer un module :
# il suffit de programmer les fonctions qui le constituent dans un ﬁchier portant le nom du modul
# On peut aussi déﬁnir des variables globales dans un module.

# 4 variables globales du module (vous pouvez en ajouter d'autres si besoin...)

import os
import shutil
import zipfile

from PIL import Image

#from resizeimage import resizeimage
# install
# https://pypi.org/project/python-resize-image/
# pip install python-resize-image

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

def choixFichier():
    global nbImage, source, nbImageMax
    
    print("nbImage=", nbImage)
    if nbImage<=18:
        source="trombi-6x3.docx"
        nbImageMax=18
    elif nbImage<=28:
        source="trombi-7x4.docx"
        nbImageMax=28
    elif nbImage<=32:
        source="trombi-8x4.docx"
        nbImageMax=32
    else:
        print("trop d'images : erreur")
        exit()


#liste des fct du module
def preparation(ledossier):
    global dossierImages, listeImage, dossierWord, source, dossier
    
    listeImage = []
    listeNomPrenom = []    # tableau de tuple ("dupond","toto")...  il faut vérifier nb de nom = nb d'images...

    # récupérer le chemin du répertoire courant
    dossierWord = os.getcwd()+"/documents/"
    dossierImages=ledossier
    dossier = ledossier

    #2. créer un dossier
    try:
        shutil.rmtree(dossierImages+'/'+'dezip')
    except:
        print('remove impossible')

    try:
        shutil.rmtree(dossierImages+'/'+'tmp')
    except:
        print('remove impossible')

    os.mkdir(dossierImages+'/'+'dezip')
    os.mkdir(dossierImages+'/'+'tmp')
    return

def copier_Images():
    pass

    
def fin(crop, listeNomPrenom, listeImages):  #    trombi.fin(crop, listeNomPrenom, listeImages)

    global dossierImages, dossierWord, dossier, source

    source="trombi-6x3.docx"
    choixFichier()  # un sur les 3 fchiers word...
    dest = "res.zip"
    shutil.copyfile(dossierWord+'/'+source, dossierImages+'/'+dest)
    #3 on dezip le fichier "res.zip"
    dezzip(dossier)

    traitementImages(crop, listeNomPrenom, listeImages)
    # on rezip
    rezip()
    
    # on detruit le dossier "dezip"
    shutil.rmtree(dossierImages+'/'+'dezip')
    os.remove(dossierImages+'/'+'res.zip')
    shutil.rmtree(dossierImages+'/'+'tmp')
    return


def quitter():
    shutil.rmtree(dossierImages+'/'+'tmp')


def images(taille):
    global dossierImages, listeImage, dossierWord, nbImageMax
    vx0,vy0,vx1,vy1=taille
    Largeur=307
    Hauteur=348

    
    print("**"+dossierImages)
    i=1
    coeff=1 #réduction de la taille des images
    #destination = dossierImages+'/'+'dezip/word/media/'
    maListe = sorted(os.listdir(dossierImages))

    for filename in maListe:
        
        f = os.path.join(dossierImages, filename)
        # images jpg
        if os.path.isfile(f):
            if filename.endswith('.jpg'):
                print("f = ",f)
                im1 = Image.open(f)
                #on cherche le bon paramètre de réduction...
                if (i==1):
                    file_stats = os.stat(f)
                    taille = file_stats.st_size
                    print("taille = ",taille)
                    coeff=1
                    if (taille>500000):
                        coeff = 2*taille//500000
                        print("coeff = ",coeff)
                    

                im1 = im1.resize((im1.width//coeff, im1.height//coeff))
                #fPng=f.replace("jpg", "png")
                nom = dossierImages+'/tmp/'+'image'+str(i)+'.png'
                im1.save(nom, format="PNG")
                #im1.save(nom)
                listeImage.append(nom)
                print("nom = ",nom)
                i=i+1
            
            # images png
            if filename.endswith('.png'):
                print(f)
                nom = dossierImages+'/tmp/'+'image'+str(i)+'.png'
                shutil.copyfile(f, nom)
                listeImage.append(nom)
                i=i+1
            
        # fichier texte
        if os.path.isfile(f) and (filename.endswith('.txt') or filename.endswith('.csv')):
            #lire le fichier NOM/prenom
            print("*")
            
        # fichier excel
        if os.path.isfile(f) and (filename.endswith('.xls') or filename.endswith('.xlsx')):
            #lire le fichier NOM/prenom
            print("*")

    print(listeImage)
    print('nb de photos:'+str(len(listeImage)))
    return listeImage

def traitementImages(crop, listeNomPrenom, listeImages):

    global dossierImages, dossierWord, nbImageMax
    print("listeNomPrenom==",listeNomPrenom)
    print("listeImages==",listeImages)
    #vx0,vy0,vx1,vy1=crop[]
    Largeur=307
    Hauteur=348

    i=1
    destination = dossierImages+'/'+'dezip/word/media/'

    for filename in listeImages:
        # images png
        print("fichier = ",filename)
        im1 = Image.open(filename)
        print("taille = ",im1.size)
        print("crop(image) = ",crop[i-1])
        
        im1=im1.crop( (crop[i-1]) )
        #im1=resizeimage.resize(im1, Largeur, Hauteur)
        nom = destination+'image'+str(i)+'.png'
        #print("img size in memory in bytes: ", sys.getsizeof(im1.tobytes()))
        im1.save(nom,optimize=True)
        #shutil.copyfile(f, destination+"image"+str(i)+'.png')
        i=i+1
    
    for reste in range(i,nbImageMax+1):
        shutil.copyfile(dossierWord+"/"+"blanc.png", destination+'image'+str(reste)+'.png')

    fichierTexte = dossierImages+'/'+'dezip/word/document.xml'
    fichierTexte3 = dossierImages+'/'+'dezip/word/document3.xml'
    with open(fichierTexte,'r') as f:
        message = f.read()
    #f.close()
    
    limite=len(listeNomPrenom)
    print("limite==",limite)
    for indice in range (0, limite):
        print("nom=",nom)
        nom, prenom = listeNomPrenom[indice]
        message = message.replace(  "Nom-"+str(indice)+"-", nom)
        message = message.replace(  "Prenom-"+str(indice)+"-", prenom)

    for indice in range (limite, nbImageMax+1, -1):
        print("nom=vide")
        message = message.replace(  "Nom-"+str(indice)+"-", "")
        message = message.replace(  "Prenom-"+str(indice)+"-", "")

    os.remove(fichierTexte)

    with open(fichierTexte,'w') as f2:
        f2.write(message)
    with open(fichierTexte3,'w') as f3:
        f3.write(message)
    #f2.close()
    


    return

def uneImage():
    global dossierImages, listeImage, dossierWord
    print(listeImage[0])
    return listeImage[0]

def lesImages():
    global listeImage
    return listeImage

                    
def dezzip(dossier):        # 
    fichier = dossier+'/'+"res.zip"
    with zipfile.ZipFile(fichier,"r") as zip_ref:
        zip_ref.extractall(dossier+'/'+"dezip")
    return
    
def rezip():            #            
    global dossierImages, listeImage, source

    src = dossierImages+"/"+'dezip'
    dest = dossierImages+"/"+source
    
    print("src = "+src)
    shutil.make_archive(dest, format='zip', root_dir=src)
    try:
        os.remove(dest)
    except:
        print("fichier déjà présent")
        
    os.rename(dest+'.zip', dest)

    return


def afficheDossierImage():
    print(dossierImages)
    return


def nbImages(dossierImages):
    global listeImage, nbImage
    print('nb de photos:'+str(len(listeImage)))
    nbImage = len(listeImage)
    return len(listeImage)

def lireFichier(fichier):
    listeNomPrenom=[] 
    dirFichier, nomFichier = os.path.split(fichier)
    nomF, extFichier = os.path.splitext(nomFichier)
    if (extFichier==".txt"):
        file  = open(fichier,"r",encoding="utf8")
        lines = file.readlines()
        for n, line in enumerate(lines) :
            if (len(line)>2):
                n,p = line.split('\t')
                listeNomPrenom.append( (n.strip(), p.strip()) )
                print(f"Ligne {n} : {line}")
        file.close()



    elif(extFichier==".xls" or extFichier==".xlsx"):
        pass

    return listeNomPrenom



