import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="EventConnect", page_icon="📅", layout="wide")

"""
input: csv1(priority sorted) is df1 and csv2(time sorted) is df2 and d
output: calendar
extra need: all csv time in that format..... 24 hour format
"""

# Center-align the title using HTML and CSS
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 24px;  /* Adjust the font size as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="centered-title">Here is your personalized calendar!!</h1>', unsafe_allow_html=True)

st.write("---")
# Function to create a block with vertical lines and links
def create_block(vertical_lines, links):
    # Create a DataFrame for Altair
    data = pd.DataFrame({
        'x': vertical_lines,
        'y': [0.5] * len(vertical_lines),
        'link': links,
        'event': [f"Event {i+1}" for i in range(len(vertical_lines))]
    })

    # Create an Altair chart
    chart = alt.Chart(data).mark_rule(color='red').encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[7, 23]), title='Time (hour)'),  # Rename x-axis
        tooltip=['link:N']
    ).properties(
        width=100,
        height=120
    ).interactive()
    
    # Add text in the middle of every vertical line
    text = alt.Chart(data).mark_text(
        align='center',
        baseline='middle',
        fontSize=15,
        color='white',
        dy=-2
    ).encode(
        x='x:Q',
        text='event:N'
    )

    # Add clickable text
    clickable_text = alt.Chart(data).mark_text(
        align='center',
        baseline='bottom',
        fontSize=12,
        color='blue',
        dy=10
    ).encode(
        x='x:Q',
        href='link:N'
    )

    # Combine the chart and text
    final_chart = chart + text + clickable_text
    return final_chart

# Example vertical lines and links for multiple blocks


df1 = pd.read_csv("priority_sorted.csv")
# Read user input data
user_input_df = pd.read_csv("user_input.csv")

# Append user input data to df1
df3 = pd.concat([df1, user_input_df], ignore_index=True)

# df2 = pd.read_csv("time_sorted.csv")
flag=0
vertical_lines=[]
links=[]
texted=[]
for i in range(len(df1)):
  if df1['Date'][i]=='':  #have to fill todays date
    if flag==0:
        index=df1['Priority index'][i]
        flag=1
    if df1['Priority index'][i]==index:
        vertical_lines.append(df1['Time'][i])
        links.append(df1['Link'][i])
        texted.append(df1['Description'][i])
    else:
        with st.container():
            left,right =st.columns([4, 1])
            with left:
                block = create_block(vertical_lines, links)
                st.altair_chart(block, use_container_width=True)
            with right:
                st.write(df1['Type'][i-1])
                for i in range(len(texted)):
                    st.write(i+1,". [{texted[i]}]({links[i]})")


df2=pd.read_csv("time_sorted.csv")
#Here to write the date input..
#Here to write last 2 special things



                




# vertical_lines1 = [0.1, 0.3, 0.5, 0.7, 0.9]
# links1 = [
#     "https://www.example.com/link1",
#     "https://www.example.com/link2",
#     "https://www.example.com/link3",
#     "https://www.example.com/link4",
#     "https://www.example.com/link5"
# ]

# vertical_lines2 = [0.2, 0.4, 0.6, 0.8]
# links2 = [
#     "https://www.example.com/link6",
#     "https://www.example.com/link7",
#     "https://www.example.com/link8",
#     "https://www.example.com/link9"
# ]

# vertical_lines3 = [0.2, 0.4, 0.6, 0.8]
# links3 = [
#     "https://www.example.com/link10",
#     "https://www.example.com/link11",
#     "https://www.example.com/link12",
#     "https://www.example.com/link13"
# ]

# # Create multiple blocks
# with st.container():
#     left,right =st.columns([4, 1])
#     with left:
#         block1 = create_block(vertical_lines1, links1)
#         st.altair_chart(block1, use_container_width=True)
#     with right:
#         st.write("asdf")

# with st.container():
#     left,right =st.columns([4, 1])
#     with left:
#         block2 = create_block(vertical_lines2, links2)
#         st.altair_chart(block2, use_container_width=True)
#     with right:
#         st.write("asdf")

# with st.container():
#     left,right =st.columns([4, 1])
#     with left:
#         block3 = create_block(vertical_lines3, links3)
#         st.altair_chart(block3, use_container_width=True)
#     with right:
#         st.write("asdf")

