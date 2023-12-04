# installation : 
# pip install --upgrade pip
# pip install Pillow
# pip install customtkinter
# pip install packaging
# 

import tkinter as tk
import tkinter.messagebox
import customtkinter    # https://customtkinter.tomschimansky.com/
import os	# pour bouton dossier http://www.python-simple.com/python-modules-fichiers/os-path.php
import tkinter.filedialog
# intaller PIL
# pip install Pillow
#
# installer imageTk sur "ubuntu":
# sudo apt-get install python3-pil.imagetk
# (jpg pas géré par défaut dans PIL !)
#
from PIL import Image, ImageTk, ImageDraw
import moduleTrombi as trombi

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

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

crop=[] # chaque élément contient 4 valeurs... x0,y0,x1,y1
listeNomPrenom=[]   # des tuples (nom, prenom)
listeImages=[]
listeSoustitres=[]
# configure window
root = customtkinter.CTk()
root.title("Trombinoscope word par Christophe Dabancourt")
root.geometry(f"{1000}x{950}")

# donne le poids de chaque colonne/ligne
root.grid_columnconfigure((0, 1, 2, 3, 4, 5 , 6, 7,8,9,10,11), weight=0)
"""root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure(( 4, 5, 6, 7, 8, 9), weight=1)"""
       
#---------------------------------------------------------- une image crop (gauche)
def imageCrop(img2, id):
    global crop

    vx0, vy0, vx1, vy1 = crop[id]

    print('img2 = ', img2.size )
    print('crop = ', (vx0,vy0,vx1,vy1) )
    img2=img2.crop( (vx0,vy0,vx1,vy1) )
    print('img2 = ', img2.size )
    width2, height2 = img2.size
    ratio = width2 / height2
    if width2>height2:
        newW=Largeur
        newH=int(ratio*newW)
    else:
        newH=Hauteur
        newW=int(ratio*newH)
    print("new = ", newH, newW)
    img2 = img2.resize( (newH,newW))
    img2 = ImageTk.PhotoImage(img2)
    return img2
#----------------------------------------------------------change image gauche
def changeImageGauche(id):
    global imageGauche, nomImageGauche, width, height, label0, scrollable_frame, scrollable_frame_switches,idImageGauche, listeImages

    idImageGauche=int(id)
    #print("photos=", photo)
    nomImageGauche = listeImages[idImageGauche]
    print("nom = ", nomImageGauche)
    imageGauche=Image.open(listeImages[idImageGauche])
    print('----------size image gauche =',imageGauche.size)
    width, height = imageGauche.size
    if width>height:
        imageGauche=Image.open(nomImageGauche).resize((int(Largeur),int(Largeur*height/width)))
        my_image = customtkinter.CTkImage(light_image=imageGauche,
                                    dark_image=imageGauche,
                                    size=(int(Largeur),int(Largeur*height/width)))
    else:
        imageGauche=Image.open(nomImageGauche).resize((int(Hauteur*width/height),int(Hauteur)))
        my_image = customtkinter.CTkImage(light_image=imageGauche,
                                    dark_image=imageGauche,
                                    size=(int(Hauteur*width/height),int(Hauteur)))
    #img1bis = ImageTk.PhotoImage(imageGauche)
    
    label3_imageGauche.configure(image=my_image)
    widthGauche, heightGauche = imageGauche.size
    x1, y1=widthGauche, heightGauche
    #associer la 1ere image au clic (bind)
    label3_imageGauche.bind("<Button-1>", event1)
    #label3_imageGauche.bind( '<Leave>', printXY)        
    print("*** fin changeImageGauche ***")
#----------------------------------------------------------change image gauche
def changeImageDroite():
    global nomImageGauche, widthGauche, heightGauche, crop, idImageGauche, width, height

    print("nomImageGauche = "+nomImageGauche)
    imageGauche=Image.open(nomImageGauche)
    print("crop ==",crop[idImageGauche])
    imageGauche=imageGauche.crop( crop[idImageGauche] )

    if width>height:
        my_image = customtkinter.CTkImage(light_image=imageGauche,
                            dark_image=imageGauche,
                            size=(int(Largeur//2),int(Largeur*height/width)))
    else:
        my_image = customtkinter.CTkImage(light_image=imageGauche,
                            dark_image=imageGauche,
                            size=(int(Hauteur*width/height),int(Hauteur//2)))
        
    label4_imageDroite.configure(image=my_image)
    print("*** fin changeImageDroite ***")
#----------------------------------------------------------change liste images BAS
def remplirScroll():
    global nomImageGauche, width, height, label0, scrollable_frame, scrollable_frame_switches
    global crop, listeSoustitres, listeImages

    #on efface l'objet...
    scrollable_frame = customtkinter.CTkScrollableFrame(root, label_text="Liste des images", height=350)
    scrollable_frame.grid(row=ligneFrame, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew", columnspan=16)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    scrollable_frame_switches = []
    listeSoustitres = []
    wf = 150
    hf = 150
    i, posX, posY = 0, 0, 0
    for photo in listeImages:
        print("chaque photo = "+photo)
        img = Image.open(photo)

        img = img.resize((wf,hf))
        draw = ImageDraw.Draw(img)
        x0,y0,x1,y1 = crop[i]
        x0,y0,x1,y1 = int(x0*wf/width), int(y0*hf/height), int(x1*wf/width), int(y1*hf/height)

        shape = [(x0, y0), (x1 ,y1 )] 
        red = (255, 0, 0)  # RGB values for red
        draw.rectangle(shape, fill=None, outline=red) 

        im1=ImageTk.PhotoImage(img)
        if (len(listeNomPrenom)==0):
            sstitre=str(i+1)
            listeSoustitres.append(sstitre.strip())
            labelTab = customtkinter.CTkLabel(master=scrollable_frame, image=im1, text=sstitre,compound='top')
        else:
            nom, prenom = listeNomPrenom[i]
            sstitre=str(i+1)+"-"+nom
            listeSoustitres.append(sstitre.strip())
            labelTab = customtkinter.CTkLabel(master=scrollable_frame, image=im1, text=sstitre, compound='top')
        posX = (i%5)*200
        if (i%5==0):
            posY=posY+200
        labelTab.grid(row=i//5, column=i%5, padx=10, pady=(0, 20))
        scrollable_frame_switches.append(labelTab)
        i = i+1
        #crop.append((0,0,w,h))
        #associer la 1ere image au clic (bind)
        labelTab.bind("<Button-1>", event2)
        labelTab.bind("<Button-3>", event2clicDroit)
    
#----------------------------------------------------------select dossier
def on_click_select_dossier():
    global nomImageGauche, width, height, label0, scrollable_frame, crop, listeImages

    # Ouvre une boîte de dialogue de sélection de dossier
    directory = tk.filedialog.askdirectory()
    trombi.preparation(directory)
    listeImages = trombi.images((vx0,vy0,vx1,vy1))

    # change le contenu du label
    label0.configure(text=directory)
    label1.configure(text = 'nombre d\'image = '+str(trombi.nbImages(directory)))

    crop=[]
    for photo in listeImages:
        img = Image.open(photo)
        w,h=img.size
        width, height = img.size
        crop.append((0,0,w,h))

    remplirScroll()

    changeImageGauche(1)
    changeImageDroite()

#----------------------------------------------------------crop l'image de gauche...
def on_click2_crop():
    global nomImageGauche, width, height, Hauteur, Largeur, vx0,vy0,vx1,vy1, idImageGauche, crop
    # générer une nouvelle image ("apres_crop.png") dans le dossier
    # afficher la 2eme image
    print("*"+label1.cget("text"))
    img2=Image.open(nomImageGauche)
    if width>height:
        img2=Image.open(nomImageGauche).resize((int(Largeur/2),int(Largeur*height/width/2)))
    else:
        img2=Image.open(nomImageGauche).resize((int(Hauteur*width/height/2),int(Hauteur/2)))
    img2=Image.open(nomImageGauche)

    vx0=int(int(f"{x0}")*width/Largeur)
    vy0=int(int(f"{y0}")*height/(Largeur*height/width))
    vx1=int(int(f"{x1}")*width/Largeur)
    vy1=int(int(f"{y1}")*height/(Largeur*height/width))

    crop[idImageGauche] = (vx0,vy0,vx1,vy1)
    print('img2 = ', img2.size )
    print('crop = ', (vx0,vy0,vx1,vy1) )
    img2=img2.crop( (vx0,vy0,vx1,vy1) )
    print('img2 = ', img2.size )
    width2, height2 = img2.size
    ratio = width2 / height2
    if width2>height2:
        newW=Largeur//2
        newH=int(ratio*newW)
    else:
        newH=Hauteur//2
        newW=int(ratio*newH)
    print("new = ", newH, newW)
    img2=img2.resize( (newH,newW))
    my_image = customtkinter.CTkImage(light_image=img2,
                    dark_image=img2,
                    size=(newH,newW))

    ###img2 = ImageTk.PhotoImage(img2)
    #label4_imageDroite.configure(image=my_image)
    crop[idImageGauche] = (vx0,vy0,vx1,vy1)
    changeImageDroite()

    remplirScroll()
    print("*** fin on_click2_crop ***")

#----------------------------------------------------------Crop ttes les images
def on_click2_crop_all():

    global width, height, Hauteur, Largeur, vx0,vy0,vx1,vy1, crop

    vx0=int(int(f"{x0}")*width/Largeur)
    vy0=int(int(f"{y0}")*height/(Largeur*height/width))
    vx1=int(int(f"{x1}")*width/Largeur)
    vy1=int(int(f"{y1}")*height/(Largeur*height/width))

    #crop[idImageGauche] = (vx0,vy0,vx1,vy1)

    for i in range(len(crop)):
        print("chaque photo = ")
        #crop[i]=(vx0,vy0,vx1,vy1)
        crop[i] = (vx0,vy0,vx1,vy1)

    #il faut changer les miages en bas...
    changeImageDroite()
    remplirScroll()

#----------------------------------------------------------sélect txt ou excel...
def on_click4_excel():
    global listeNomPrenom
    filename = tk.filedialog.askopenfilename(initialdir= ".",title="Choisir la liste des étudiants",filetypes=(("étudiant","*.xls"),("étudiant","*.xlsx"),("étudiant","*.txt"))) 
    listeNomPrenom = trombi.lireFichier(filename)
    print(filename)
    if (len(listeNomPrenom)==0):    # liste vide
        return
    if (len(listeNomPrenom)<len(crop)):
        pass
    elif (len(listeNomPrenom)>len(crop)):
        remplirScroll()
    else:
        remplirScroll()
#----------------------------------------------------------Crop ttes les images
def on_click3_word():
    #global crop
    print("*** WORD")
    #trombi.traitementImages(crop)
    trombi.fin(crop, listeNomPrenom, listeImages)
#----------------------------------------------------------fin fct


ligne = 0
button1 = customtkinter.CTkButton(root, text="1. Dossier des images", command=on_click_select_dossier )
button1.grid(row=ligne, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

label0 = customtkinter.CTkLabel(master=root, justify=customtkinter.LEFT, text=os.getcwd())
label0.grid(row=ligne, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

ligne = ligne + 1
label1 = customtkinter.CTkLabel(master=root, justify=customtkinter.LEFT, text='nombre d\'image =')
label1.grid(row=ligne, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

#label2 = customtkinter.CTkLabel(master=root, justify=customtkinter.LEFT, text="cliquer pour faire la cadre")
#label2.grid(row=ligne, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

ligne = ligne + 1
x0,y0,x1,y1=0,0,0,0

img1 = Image.open("documents/blanc.png")
img1 = customtkinter.CTkImage(light_image=img1,
                                dark_image=img1,
                                size=(30, 30))

label3_imageGauche = customtkinter.CTkLabel(master=root, justify=customtkinter.LEFT, image=img1, text="")
label3_imageGauche.grid(row=ligne, column=0)

label4_imageDroite = customtkinter.CTkLabel(master=root, justify=customtkinter.LEFT, image=img1, text="")
label4_imageDroite.grid(row=ligne, column=1)

#button6Ajouter = customtkinter.CTkButton(root, text="+", command=on_click2_crop, height=30, width=30, font=('',20))
#button6Ajouter.grid(row=ligne, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")


# Ajoute le champ de saisie-----------------------------------------------

ligne = ligne + 1
button2Crop = customtkinter.CTkButton(root, text="2. CROP de l'image", command=on_click2_crop)
button2Crop.grid(row=ligne, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

button3Crop = customtkinter.CTkButton(root, text="3. CROP de toutes les images", command=on_click2_crop_all)
button3Crop.grid(row=ligne, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

# Ajoute le bouton fichier des noms --------------------------------------------

#ligne = ligne + 1
button2Crop = customtkinter.CTkButton(root, text="4. Liste des étudiants (txt/xls/xlsx)", command=on_click4_excel)
button2Crop.grid(row=ligne, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

# create scrollable frame-----------------------------------------------
ligne = ligne + 1
ligneFrame = ligne
scrollable_frame = customtkinter.CTkScrollableFrame(root, label_text="Liste des images", height=350)
scrollable_frame.grid(row=ligne, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew", columnspan=16)
scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame_switches = []
i, posX, posY = 0, 0, 0

# Ajoute le champ de saisie-----------------------------------------------
ligne = ligne + 1
button2Crop = customtkinter.CTkButton(root, text="5. créer le fichier WORD", command=on_click3_word, fg_color='green')
#button2Crop.grid(row=ligne, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
button2Crop.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

# image de gauche cliquée -----------------------------------------------
def printXY(event):
    global x0,y0,x1,y1,x2,y2,width,height, imageGauche, idImageGauche, nomImageGauche
    x2 = event.x
    y2 = event.y
    #print("clic: ",x2,y2)
    if (x2>x0 or y2>y0):
        imageGauche=Image.open(nomImageGauche)

        imageGaucheSave = imageGauche
        imageGaucheSave=imageGaucheSave.resize((int(Largeur),int(Largeur*height/width)))
        if (x2-x0>y2-y0):
            draw = ImageDraw.Draw(imageGaucheSave)
            #imageGaucheSave=imageGauche
            y2=int(y0+(Hauteur*(x2-x0)/Largeur))
            shape = [(x0, y0), (x2 ,y2 )] 
        else:
            draw = ImageDraw.Draw(imageGaucheSave)
            #imageGaucheSave=imageGauche
            x2=int(x0+(Largeur*(y2-y0)/Hauteur))
            shape = [(x0, y0), (x2 ,y2 )] 
        
        red = (255, 0, 0)  # RGB values for red

        draw.rectangle(shape, fill=None, outline=red) 
        #width, height = imageGauche.size
        if width>height:
            my_image = customtkinter.CTkImage(light_image=imageGaucheSave,
                                        dark_image=imageGaucheSave,
                                        size=(int(Largeur),int(Largeur*height/width)))
        else:
            #imageGauche=Image.open(nomImageGauche).resize((int(Hauteur*width/height),int(Hauteur)))
            my_image = customtkinter.CTkImage(light_image=imageGaucheSave,
                                        dark_image=imageGaucheSave,
                                        size=(int(Largeur),int(Largeur*height/width)))
        #img1bis = ImageTk.PhotoImage(imageGauche)
        
        label3_imageGauche.configure(image=my_image)




# image de gauche cliquée -----------------------------------------------
def event1(event):
    global numPoint,x0,y0,x1,y1,width,height,x2,y2
    numPoint=(numPoint+1)%2
    #print("numPoint=",numPoint)
    x = event.x
    y = event.y
    #print("clic: ",x,y, Hauteur)
    if (y<Hauteur//4):
        x0,y0=x,y
        label3_imageGauche.bind('<Motion>', printXY)        

    else:
        x1,y1=x2,y2
        label3_imageGauche.unbind( '<Motion>')

    coeff=(int(f"{y1}")-int(f"{x1}"))/(int(f"{y0}")-int(f"{x0}"))*Hauteur/Largeur
    changeImageDroite()
    #print("fin clic")

# image du bas (liste) cliquée -----------------------------------------------
def event2(event):
    print("*** debut event2 ***")
    caller = event.widget
    sousTitre = caller.cget("text")
    indice=listeSoustitres.index(sousTitre)
    changeImageGauche(indice)
    changeImageDroite()
    nomImage=caller.cget("image")
    print("listeSoustitres = ",listeSoustitres)
    print("listeImages = ",listeImages)
    print("crop = ",crop)
    print("listeNomPrenom = ",listeNomPrenom)
    
    print("*** fin event2 ***")
    
# image du bas (liste) cliquée ----- les actions ------------
def supprimer():
    global listeSoustitres, crop, idImageGauche, listeImages
    print("sousTitre=",sousTitre)
    indice=listeSoustitres.index(sousTitre)
    print("indice=",indice)
    del(listeImages[indice])
    del(crop[indice])
    if (len(listeNomPrenom)>0):
        del(listeNomPrenom[indice])
    if(idImageGauche>=indice):
        idImageGauche=max(0,indice-1)
        changeImageGauche(idImageGauche)
        changeImageDroite()
    remplirScroll()
    label1.configure(text = 'nombre d\'image = '+str(len(listeImages)))

def echangeAvant():
    global listeSoustitres, listeImages, crop, idImageGauche
    indice=listeSoustitres.index(sousTitre)
    print("indice=",indice)
    if (indice==0):
        return
    listeImages[indice-1], listeImages[indice] = listeImages[indice], listeImages[indice-1]
    crop[indice-1], crop[indice] = crop[indice], crop[indice-1]
    remplirScroll()
    
def echangeApres():
    global listeSoustitres, listeImages, crop, idImageGauche
    indice=listeSoustitres.index(sousTitre)
    if (indice==len(listeImages)):
        return
    listeImages[indice+1], listeImages[indice] = listeImages[indice], listeImages[indice+1]
    crop[indice+1], crop[indice] = crop[indice], crop[indice+1]
    remplirScroll()
    
# image du bas (liste) cliquée ----- menu deroulant ---------
m = tk.Menu(root, tearoff = 0)
m.add_command(label ="supprimer", command=supprimer)
m.add_command(label ="vers le début", command=echangeAvant)
m.add_command(label ="vers la fin", command=echangeApres)
m.add_separator()
m.add_command(label ="Rename")
# image du bas (liste) cliquée -----------------------------------------------
def event2clicDroit(event):
    global sousTitre
    print("*** debut event2d ***")
    caller = event.widget
    sousTitre = caller.cget("text")
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
    print("*** fin event2d ***")
    
# fin du programme -----------------------------------------------
def on_closing():
    #supprimer les fichiers temporaires...
    try:
        trombi.quitter()
    except:
        print("erreur de fin...")
    root.destroy()

#----------------------------------------------------------
# Intercepter l'événement on_closing
root.protocol("WM_DELETE_WINDOW", on_closing)
#******************************************************************
# Lance la boucle d'événements-------------------------------------
root.mainloop()
