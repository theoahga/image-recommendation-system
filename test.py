from sklearn import tree
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json
import random
import ipywidgets as widgets
from IPython.display import display, clear_output

def extract_data_from(path):
    with open(path, 'r') as file:
        return json.load(file)


def extract_matrix():
    matrix = []


    tags = extract_data_from('./content/tags.json')
    exifs = extract_data_from('./content/exif.json')
    dominants_colors = extract_data_from('./content/dominants_colors.json')

    for image in tags:
        image_name = os.path.basename(image)

        
        image_tags = tags[image]

        exif = {}
        if image_name in exifs and exifs[image_name] is not None:
            exif = exifs[image_name]

        if image_name in dominants_colors and dominants_colors[image_name] is not None:
            dominant_color = dominants_colors[image_name]

        orientation = 0
        if 'Orientation' in exif and exif['Orientation'] is not None:
            orientation = exif['Orientation'] 


        petit = 0 if image_tags["petit"] == "false" else 1
        moyen = 0 if image_tags["moyen"] == "false" else 1
        grand = 0 if image_tags["grand"] == "false" else 1
        court = 0 if image_tags["poils courts"] == "false" else 1
        long = 0 if image_tags["poils long"] == "false" else 1
        tomb = 0 if image_tags["oreilles tombantes"] == "false" else 1
        releves = 0 if image_tags["oreilles relevÃ©s"] == "false" else 1
        nez_plat = 0 if image_tags["museau plat"] == "false" else 1
        nez_moyen = 0 if image_tags["museau moyen"] == "false" else 1
        nez_alonge = 0 if image_tags["museau alongÃ©"] == "false" else 1

        node = [
            petit,
            moyen,
            grand,
            court,
            long,
            tomb,
            releves,
            nez_plat,
            nez_moyen,
            nez_alonge,
            orientation,
            dominant_color[0],
            dominant_color[1],
            dominant_color[2]
            ]

        

        matrix.append(node)

    return matrix

def pick_random_images(path, nb):
    files = os.listdir(path)
    return random.sample(files, nb)
    


class ImageRatingApp:
    def __init__(self, image_list):
        self.image_list = image_list
        self.current_index = 0
        self.ratings = {}
        self.output = widgets.Output()
        self.image_widget = widgets.Image(value=self.image_list[self.current_index], width=300, height=300)
        self.rating_dropdown = widgets.Dropdown(options=['Favori', 'Non favori'], description='Note : ')
        self.next_button = widgets.Button(description='Suivant')
        self.next_button.on_click(self.next_image)
        
        self.update_output()
        
    def update_output(self):
        with self.output:
            clear_output(wait=True)
            display(self.image_widget)
            display(self.rating_dropdown)
            display(self.next_button)
            
    def next_image(self, b):
        self.ratings[self.current_index] = self.rating_dropdown.value
        self.current_index += 1
        if self.current_index < len(self.image_list):
            self.image_widget.value = self.image_list[self.current_index]
            self.rating_dropdown.value = None
        else:
            self.close_app()
            
    def close_app(self):
        with self.output:
            clear_output(wait=True)
            print("Merci d'avoir noté toutes les images.")
        



def main():
    # The vector extraction
    data = extract_matrix()
    print(data)
    dataframe = pd.DataFrame(data, columns=["petit", "moyen", "grand", "poils courts", "poils long", "oreilles tombantes", "oreilles relevés", "museau plat", "museau moyen", "museau alongé", "orientation", "red", "green", "blue"])

    # Random images pick up
    selected_images = pick_random_images("./content/images",7)

    # Rating app launch
    app = ImageRatingApp(selected_images)
    display(app.output)

    print("fini")

if __name__ == "__main__":
    main()



# result = [
#     "Favorite",
#     "NotFavorite",
#     "Favorite",
#     "Favorite",
#     "Favorite",
#     "Favorite",
#     "Favorite",
#     "NotFavorite",
#     "NotFavorite",
#     "Favorite",
#     "Favorite",
#     "NotFavorite",
#     "NotFavorite",
# ]

# # Création de dataframes
# resultframe = pd.DataFrame(result, columns=["favorite"])

# # Convertir les valeurs booléennes en valeurs numériques
# for col in ["petit", "moyen", "grand", "poils courts", "poils long", "oreilles tombantes", "oreilles relevés", "museau plat", "museau moyen", "museau alongé"]:
#     le = LabelEncoder()
#     dataframe[col] = le.fit_transform(dataframe[col])

# # Générer des étiquettes numériques
# le = LabelEncoder()
# resultframe["favorite"] = le.fit_transform(resultframe["favorite"])

# # Utilisation du classificateur d'arbre de décision
# dtc = tree.DecisionTreeClassifier()
# dtc = dtc.fit(dataframe.to_numpy(), resultframe.values.ravel())

# # Prédiction pour une nouvelle image de chien
# nouvelle_image = [[False, True, True, True, False, False, False, False, False, True, 0, 255, 0, 255]]  # Exemple de nouvelle image
# prediction = dtc.predict(nouvelle_image)
# print(dtc.predict_proba(nouvelle_image).max(axis=1).mean())
# print("Prédiction pour la nouvelle image:", le.inverse_transform(prediction))
# print("Poids des attributs :", dtc.feature_importances_)