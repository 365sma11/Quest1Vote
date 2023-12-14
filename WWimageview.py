import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64

# Initialize Streamlit app
st.title('WW Quest 1- Submissions Viewer')

# Step 1: Update dropdown options
option = st.sidebar.selectbox('Select Option', ('Community', 'Team'))

# Step 2: Conditional CSV file loading
if option:
    st.write("Hover over image/video for expander to click")
    csv_file = f'{option.lower()}.csv'
    
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)

        # Determine the number of columns based on screen width
        max_width = 300  # Assume a default max width per image/video
        screen_width = 1200  # Default screen width or use JS to get actual width
        num_columns = max(1, screen_width // max_width)
        cols = st.columns(num_columns)

        # Step 3: Process CSV data and dynamically fill columns
        col_index = 0
        for index, row in data.iterrows():
            file_path = os.path.join(f'./{option.lower()}', row['File'])
          
            if os.path.exists(file_path):
                current_col = cols[col_index % num_columns]
                
                if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                    image = Image.open(file_path)
                    current_col.image(image, caption=f"{row['Team']} - Entry: {row['Entry']}", use_column_width=True)
                elif file_path.endswith('.mp4'):
                    # current_col.video(file_path)
                    video_file = open(file_path, 'rb')
                    video_bytes = video_file.read()
                    b64_video = base64.b64encode(video_bytes).decode()

                    # Embed the video using HTML with appropriate CSS
                    current_col.markdown(f"""
                        <div style="padding: 10px; text-align: center;">
                            <video style="max-width: 100%; height: auto;" controls>
                                <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
                            </video>
                        </div>
                        """, unsafe_allow_html=True)

                # Center the link and add a horizontal line
                current_col.markdown(f"<center><a href='{row['Link']}'>X Link</a></center>", unsafe_allow_html=True)
                current_col.markdown("---")

                col_index += 1
    else:
        st.write(f"No data available for {option}")

