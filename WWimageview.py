import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64

# Initialize Streamlit app
st.title('WW Quest 1- Submissions Viewer')

# Step 1: Update dropdown options
option = st.sidebar.selectbox('Select Option', ('Community', 'Team'))
vote = "https://pn2nq2l5rqu.typeform.com/to/yYL4jCdC"
st.sidebar.markdown(f"<center><a href='{vote}'>Go Vote</a></center>", unsafe_allow_html=True)

# Step 2: Conditional CSV file loading
if option:
    st.write("Hover over image/video for expander to click")
    st.write("Note: mobile sound does not work for video- click X Link to watch on X")
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
                
                # Display image or video
                if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                    image = Image.open(file_path)
                    current_col.image(image, use_column_width=True)
                elif file_path.endswith('.mp4'):
                    current_col.video(file_path)

                # Display caption, team, entry, and link consistently
                caption = f"{row['Team']} - Entry: {row['Entry']}"
                current_col.markdown(f"<div style='text-align: center;'>{caption}</div>", unsafe_allow_html=True)
                current_col.markdown(f"<center><a href='{row['Link']}'>X Link</a></center>", unsafe_allow_html=True)
                current_col.markdown("---")

                col_index += 1
    else:
        st.write(f"No data available for {option}")
