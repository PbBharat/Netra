import streamlit as st
from PIL import Image

def main():
    st.title("Image Upload and Audio Play App")

    # Image upload
    uploaded_image = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    if st.button("Get answer"):
        # Display the image
        # image = Image.open(uploaded_image)
        # st.image(image, caption='Uploaded Image.', use_column_width=True)
        # st.write("Here's the text related to the uploaded image!")

        # if st.button("Play Audio"):

            # Display an audio player widget to play audio
            audio_file = open('/home/aneesh.paul/Documents/Repos/searce_hackathon/backend/output.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3', start_time=0)

if __name__ == "__main__":
    main()
