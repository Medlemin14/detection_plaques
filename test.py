import torch
import os

model_path = 'C:\\Users\\hp\\Desktop\\SID\\Projects\\detection_plaques\\yolov5\\runs\\train\\exp5\\weights\\best.pt'
device = torch.device('cpu')  # Ou 'cuda' si vous avez configuré CUDA correctement

try:
    # Charger le modèle directement avec torch.load
    model = torch.load(model_path, map_location=device)

    # Instancier le modèle YOLOv5 (vous devrez peut-être ajuster cela en fonction de votre version de YOLOv5)
    # Ceci est une approximation, vous devrez peut-être adapter cette partie.
    model = model['model']  # Si votre modèle est enregistré comme un dictionnaire
    model.to(device).eval()  # Déplacer vers le CPU/GPU et mettre en mode évaluation

except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    exit()

image_paths = ['annonce_8_5_5.jpg', 'annonce_8_5_6.jpg']
image_paths = [os.path.abspath(p) for p in image_paths]
print(f"Images a traiter: {image_paths}")

try:
    # Préparer les images pour l'entrée du modèle (vous devrez peut-être adapter cela)
    img = [torch.randn(3, 640, 640).to(device) for _ in image_paths] #Exemple d'entrée
    #Il faudra adapter le préprocessing de l'image : redimensionnement, normalisation, etc.

    # Effectuer l'inférence
    with torch.no_grad(): # Desactiver le calcul du gradient
        results = model(img)

    # Analyser et afficher les résultats (vous devrez adapter cela)
    print(results) #Affiche les résultats bruts.  Il faudra les interpreter.

except Exception as e:
    print(f"Erreur lors de la détection: {e}")
