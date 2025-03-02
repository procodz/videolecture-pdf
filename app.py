import os
import cv2
import img2pdf
import streamlit as st
from yt_dlp import YoutubeDL

# Function to download YouTube video
def download_youtube_video(url, output_path="video.mp4"):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

# Function to extract frames at intervals
def extract_frames(video_path, output_folder, interval_seconds=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)
    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    return output_folder

# Function to create PDF from images
def create_pdf_from_images(image_folder, output_pdf):
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.endswith(".jpg")]
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(images))
    st.success(f"PDF generated: {output_pdf}")

# Streamlit UI
def main():
    st.title("YouTube Lecture to PDF Converter")
    st.write("This app converts a YouTube lecture video into a PDF of screenshots.")

    # Input fields
    youtube_url = st.text_input("Enter YouTube Video URL:")
    interval_seconds = st.number_input("Enter the interval between screenshots (in seconds):", min_value=1, value=10)
    output_pdf = st.text_input("Enter the output PDF filename (e.g., lecture.pdf):", "lecture.pdf")

    if st.button("Generate PDF"):
        if youtube_url and output_pdf:
            with st.spinner("Downloading video..."):
                video_path = download_youtube_video(youtube_url)
                if video_path:
                    with st.spinner("Extracting frames..."):
                        image_folder = "frames"
                        extract_frames(video_path, image_folder, interval_seconds)
                    with st.spinner("Creating PDF..."):
                        create_pdf_from_images(image_folder, output_pdf)
                    st.balloons()
                    st.success("PDF generation complete!")
                    st.write(f"Download the PDF: [{output_pdf}]({output_pdf})")
        else:
            st.warning("Please provide a valid YouTube URL and output PDF filename.")

# Run the app
if __name__ == "__main__":
    main()