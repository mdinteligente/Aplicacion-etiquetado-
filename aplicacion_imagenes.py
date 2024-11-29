import streamlit as st
import os
import pandas as pd
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import numpy as np
from sklearn.metrics import cohen_kappa_score

# Google Drive API Setup
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "aplicacion-ica-icb-071024",
    "private_key_id": "46e7f30ebaafa949d1f38ac4913f0b721241c142",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDIOphXI/gZQEoA\nxKKTO45bYDK40dcDhq+AUZgLg6v0h9GaqAGUMaHtocSUaEU8RGLYc6Z8b68zezaD\nZv/gX5DI1XyDW/dBeuApwhFXe1OpW5AUKk4caxp2UFbWI2HPkbfAdANne0toPP5z\nEiGYRMylwIbq9l92YqIBwWiyxDy5LCsCKQ7kSbwWnsTLIFguoLcWbdtVvvOi2rLf\nEzo0qPpq2IutrqdJdXv/BCzK4l3A5j9YA3WAQNNNeEPY0gFJkjYUCc9zhuepGIOS\nD9XaNmA4lkosX4hjBLlYKtnMKTNiYdLxkAryEkI9fH+Vxy46DJk0LOCSPuy+33+p\nltmymBSbAgMBAAECggEAE4wU3zz1tZFfKCAKNxFzXlxP11c1BHUboQ1WKJmcKe0w\ne0a3kL4frtFCHbLoP2/1rmfr8u38TqxSsBVYGZF60wB0fWZ3Bv917t2xT7cMfdYg\nhLd0lLWoCbDiKVme7OKu66znwCx7OhvqQ1Wbzf+5ct0OztVqkGYkpsM482rQ+sq2\nmo5jI6cdaQ98Ocgxj9Xne84Q++5cT3h5OIRheW4KRsur5suP6VMD8it4SNYTIbVr\nRwv3tdUajfBReWqk+I2JFPLwpsFwqWhdPQIKI0YC5JX9aNfUTDWCwgGPy3YneOih\n9W2IvXsKcQcZkcWvSx04gH0uLkva1QXD0SkxtUAJUQKBgQD7/zeLxpJKwHmIKQb7\nEbLmI1cG4Zj8tcPPEL2mhZLxYnD4JHWt9r+eO+egs+BYrheekX2//MqNRClbRnrh\nfu68HCGn1cXjn8cIf4eVnUcyS5betSMnLc7uWwMtiyKImuw3eprVgzrxN1nLnAOr\n38+dUTt8MZsMFI5swTM2bLb7zwKBgQDLaNsJjnYuB0j04U1TgkMR8QbLF0P22lUK\nqJQTpshsOvuDwJ8Ou/x6Pl+XCoJ2E9NPXxSF/JZZHuFMNqB92mIcUdqlgftMGuH6\n5b9DJXsi8D5R0w4UYd8qzFOx0JfLi/8itFt5VWbibTni6llF+07YSXe6L2xgB66W\n6XgW5C3RdQKBgCW9YD0/vPMTBmB8/H2ndep/im4OZVIbirq9IBoLUSlze8W9+B3Y\noXP6NsNbjRLa59Coq3OQUWl8ttDjqk2RLAHiGKxBGMTxTeaY6t5eUqZWqb6q1Bvv\nAVmzKbOtbbuVsCDS7NNjNvWfO4SB1g7skvRVkRoVd8oEXhwthxT0jScDAoGAMF5e\nt4cI0ykoUBLDMHhpOnr2ApUltC12y3IKxCGExze/VzUWnYpWHzt1v5TgMPPF67nQ\nR4wotEiDinvy7fpgGhvcwj6GYzKBSggX0v+2qDg4mXx2fKJJTwQHYuEXN2+y263H\nkrKcJHuUqEDRubJorUXLEpr0SmGJQpmB1O+tdYECgYAebt2pdPhjTu9g6wO3H91P\naiDhH0+0xOCQot9FD0UgPvsv7aDHSkuqWsE8nLFRBQoH+AxQWYw/ScjIAgBe7Dl8\nt3QIRR+WXFe9dekpyKZ1bW6yHESXCScN/fet+On9La288lps6yDY/Gf2RKHR0B3Z\nlpd5jmMe1BKuI9g+orXhzg==\n-----END PRIVATE KEY-----\n",
    "client_email": "streamlit-drive-access@aplicacion-ica-icb-071024.iam.gserviceaccount.com",
    "client_id": "113339940456940358273",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-drive-access%40aplicacion-ica-icb-071024.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
SCOPES = ["https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Function to fetch image file from Google Drive
def get_image_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return Image.open(file_io)

# Function to upload file to Google Drive
def upload_file_to_drive(file_name, file_path, folder_id):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='text/csv')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Load list of images (IDs or names and corresponding Google Drive IDs)
image_list = pd.read_csv("images_list.csv")  # CSV file containing image file names and their Google Drive IDs

# Streamlit Application
st.title("Clasificación de Imágenes de Heridas Quirúrgicas")

# Authentication
username = st.text_input("Usuario:")
password = st.text_input("Contraseña:", type="password")

if username == "icbunab25" and password == "heridas":
    st.write("Por favor, clasifique las siguientes imágenes como 'alteradas' o 'no alteradas'.")

    # Display an image for labeling
    if 'current_image_index' not in st.session_state:
        st.session_state.current_image_index = 0

    image_index = st.session_state.current_image_index

    if image_index < len(image_list):
        image_id = image_list.iloc[image_index]['drive_id']
        image_name = image_list.iloc[image_index]['file_name']
        image = get_image_from_drive(image_id)
        st.image(image, caption=image_name, use_column_width=True)

        # Labeling options
        expert = st.selectbox("Seleccione su rol:", ('Cirujano', 'Dermatólogo', 'Enfermera'))
        label = st.radio("Seleccione la clasificación de la herida:", ('Alterada', 'No alterada'))
        
        additional_labels = []
        if label == 'Alterada':
            st.write("Seleccione todas las características que apliquen:")
            additional_labels = st.multiselect("Características de la herida alterada:", [
                "Bordes dehiscentes",
                "Bordes macerados",
                "Edema más allá del borde de la herida",
                "Enrojecimiento patológico",
                "Sangrado/Equimosis/Hematoma",
                "Tejido necrótico",
                "Supuración",
                "Vesículas o ampollas",
                "Tractos fistulosos",
                "Cicatriz hipertrófica"
            ])
        
        # Save labels
        if st.button("Guardar clasificación"):
            result = {
                "image_name": image_name,
                "expert": expert,
                "label": 1 if label == 'Alterada' else 0,
                "additional_labels": additional_labels
            }
            results_df = pd.DataFrame([result])
            if os.path.exists("classification_results.csv"):
                results_df.to_csv("classification_results.csv", mode='a', header=False, index=False)
            else:
                results_df.to_csv("classification_results.csv", index=False)
            
            st.session_state.current_image_index += 1
            st.success("Clasificación guardada exitosamente.")

        # Calculate and display inter-expert agreement dynamically
        if os.path.exists("classification_results.csv"):
            df = pd.read_csv("classification_results.csv")
            classification_table = df.pivot_table(index='image_name', columns='expert', values='label', aggfunc='first')
            st.subheader("Índice de Acuerdo entre Expertos (Cálculo Dinámico)")
            if len(classification_table.columns) == 3:
                labels = classification_table.dropna()
                if not labels.empty:
                    kappa_1_2 = cohen_kappa_score(labels.iloc[:, 0], labels.iloc[:, 1])
                    kappa_1_3 = cohen_kappa_score(labels.iloc[:, 0], labels.iloc[:, 2])
                    kappa_2_3 = cohen_kappa_score(labels.iloc[:, 1], labels.iloc[:, 2])
                    average_kappa = np.mean([kappa_1_2, kappa_1_3, kappa_2_3])
                    st.write(f"Cohen's Kappa entre Cirujano y Dermatólogo: {kappa_1_2:.2f}")
                    st.write(f"Cohen's Kappa entre Cirujano y Enfermera: {kappa_1_3:.2f}")
                    st.write(f"Cohen's Kappa entre Dermatólogo y Enfermera: {kappa_2_3:.2f}")
                    st.write(f"Índice de Acuerdo Promedio (Cohen's Kappa): {average_kappa:.2f}")
                else:
                    st.write("No hay suficientes datos para calcular el índice de acuerdo.")
    else:
        st.write("Todas las imágenes han sido clasificadas.")

    # Display Summary Tables if all images are classified
    if os.path.exists("classification_results.csv"):
        st.write("\n---\n")
        st.header("Resultados de Clasificación")
        df = pd.read_csv("classification_results.csv")

        # Create a pivot table for classification comparison
        classification_table = df.pivot_table(index='image_name', columns='expert', values='label', aggfunc='first')
        st.subheader("Tabla Comparativa de Clasificaciones (Alteradas vs No Alteradas)")
        st.dataframe(classification_table.fillna('-'))
        classification_table.to_csv("classification_table.csv")
        upload_file_to_drive("classification_table.csv", "classification_table.csv", "1ee1fWDPfGklA7C1894VaAfa5P0-duNCl")

        # Create a table for additional labels (reasons for altered wounds)
        altered_wounds = df[df['label'] == 1]
        additional_labels_table = altered_wounds.explode('additional_labels').pivot_table(
            index='image_name', columns='additional_labels', aggfunc='size', fill_value=0
        )
        st.subheader("Características de las Heridas Alteradas")
        st.dataframe(additional_labels_table)
        additional_labels_table.to_csv("additional_labels_table.csv")
        upload_file_to_drive("additional_labels_table.csv", "additional_labels_table.csv", "YOUR_DRIVE_FOLDER_ID")

        # Calculate inter-expert agreement after all images are classified
        if len(classification_table.columns) == 3:
            st.subheader("Índice de Acuerdo entre Expertos (Resumen Final)")
            labels = classification_table.dropna()
            if not labels.empty:
                kappa_1_2 = cohen_kappa_score(labels.iloc[:, 0], labels.iloc[:, 1])
                kappa_1_3 = cohen_kappa_score(labels.iloc[:, 0], labels.iloc[:, 2])
                kappa_2_3 = cohen_kappa_score(labels.iloc[:, 1], labels.iloc[:, 2])
                average_kappa = np.mean([kappa_1_2, kappa_1_3, kappa_2_3])
                st.write(f"Cohen's Kappa entre Cirujano y Dermatólogo: {kappa_1_2:.2f}")
                st.write(f"Cohen's Kappa entre Cirujano y Enfermera: {kappa_1_3:.2f}")
                st.write(f"Cohen's Kappa entre Dermatólogo y Enfermera: {kappa_2_3:.2f}")
                st.write(f"Índice de Acuerdo Promedio (Cohen's Kappa): {average_kappa:.2f}")
            else:
                st.write("No hay suficientes datos para calcular el índice de acuerdo.")
else:
    st.error("Usuario o contraseña incorrectos. Por favor, intente de nuevo.")
