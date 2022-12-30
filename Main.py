import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp

def choose_file(label : tk.Label = None):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])

    if label:
        if file_path == "":
            label["text"] = "Aucun fichier sélectionné"
        else:
            label["text"] = file_path
    check()
    return file_path

def choose_folder(label : tk.Label = None):
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory()

    if label:
        if folder_path == "":
            label["text"] = "Aucun répertoire sélectionné"
        else:
            label["text"] = folder_path

    check()
    return folder_path

def split_video(file_path, dest_folder_path,duration):

    video_to_split = mp.VideoFileClip(file_path)
    name_video_to_split = video_to_split.filename.split("/")[-1].split(".")[0]
    print (name_video_to_split)
    try:
        duration = int(duration)
    except:
        print("La durée doit être un nombre entier")
        return

    # Détermine le nombre de parties dans la vidéo en divisant la durée totale de la vidéo par la durée de chaque partie
    num_parts = int(video_to_split.duration // duration) + 1

    print(f"La vidéo sera divisée en {str(num_parts)} parties.")

    for i in range(num_parts):
        start_time = i * duration
        print (f"La partie {str(i+1)} commencera à {str(start_time)} secondes.")
        end_time = start_time + duration
        print (f"La partie {str(i+1)} se terminera à {str(end_time)} secondes.")

        # Vérifie si la fin de la partie dépasse la durée totale de la vidéo
        if end_time > video_to_split.duration:
            end_time = video_to_split.duration

        try:
            part = video_to_split.subclip(start_time, end_time)
        except:
            print(f"ERREUR : La partie {str(i+1)} n'a pas pu être créée.")
            return
        try:
            part.write_videofile(dest_folder_path + f"/part{i}.mp4")
        except:
            print(f"ERREUR : La partie {str(i+1)} n'a pas pu être enregistrée.")
            return
    print(f"La vidéo a été divisée avec succès.")
    return


def check():
    if file_path_label["text"] != "Aucun fichier sélectionné" and dest_folder_path_label["text"] != "Aucun répertoire sélectionné" and seconds.get() != "":
        split_button.config(state="normal")
    else:
        split_button.config(state="disabled")

def main():

    global window
    window = tk.Tk()
    window.geometry("600x400")
    window.title("VideoSplitter")
    window.iconbitmap("src/VideoSplitter.ico")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)


    global file_path_label
    global dest_folder_path_label

    # Création d'un label qui contiendra le chemin absolu du fichier à diviser
    file_path_label = tk.Label(window, text="Aucun fichier sélectionné", font=("Arial", 8, "italic"))
    # Création d'un label qui contiendra le chemin absolu du répertoire de destination
    dest_folder_path_label = tk.Label(window, text="Aucun répertoire sélectionné", font=("Arial", 8, "italic"))
    # Création d'un label qui contiendra la durée de chaque partie
    duration_label = tk.Label(window, text="Durée de chaque partie (en secondes)", font=("Arial", 8, "bold"))

    # Création d'un bouton 'Fichier' qui ouvre une fenêtre de dialogue pour choisir le fichier à diviser
    file_button = tk.Button(window, text="Fichier", command=lambda: choose_file(file_path_label))
    file_button.place(relx=0.3, rely=0.2, anchor="nw")
    file_path_label.place(relx=0.5, rely=0.2, anchor="nw")

    # Création d'un bouton "Parcourir" pour choisir le répertoire de destination
    dest_folder_button = tk.Button(window, text="Parcourir", command=lambda : choose_folder(dest_folder_path_label))
    dest_folder_button.place(relx=0.3, rely=0.3, anchor="nw")
    dest_folder_path_label.place(relx=0.5, rely=0.3, anchor="nw")


    ## Création d'un champ de saisie.
    global seconds
    seconds = tk.Entry(window, width=10)
    seconds.place(relx=0.5, rely=0.4, anchor="nw")
    duration_label.place(relx=0.1, rely=0.4, anchor="nw")
    seconds.bind("<KeyRelease>", lambda event: check())

    # Création d'un bouton "Diviser" qui divise la vidéo en parties
    global split_button
    split_button = tk.Button(window, text="Diviser")
    split_button.config(width=40)
    split_button.config(state="disabled")
    split_button.place(relx=0.3, rely=0.5, anchor="nw")
    split_button.config(command=lambda: split_video(file_path_label["text"], dest_folder_path_label["text"], seconds.get()))

    # Création d'un bouton "Quitter" qui ferme la fenêtre de couleur rouge en police blanche gras
    quit_button = tk.Button(window, text="Quitter", command=window.destroy, bg="red", fg="white", font=("Arial", 8, "bold"))
    quit_button.config(width=40)
    quit_button.place(relx=0.3, rely=0.6, anchor="nw")

    window.mainloop()


main()
