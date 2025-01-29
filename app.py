import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

def create_wordcloud(text, additional_stopwords=None, max_words=None, width=800, height=400):
    """
    Creates a word cloud from input text
    """
    # Basic list of Italian articles and common words
    italian_stopwords = {
        'il', 'lo', 'la', 'i', 'gli', 'le',  # articoli determinativi
        'un', 'uno', 'una',                   # articoli indeterminativi
        'del', 'dello', 'della', 'dei', 'degli', 'delle',  # preposizioni articolate
        'al', 'allo', 'alla', 'ai', 'agli', 'alle',
        'dal', 'dallo', 'dalla', 'dai', 'dagli', 'dalle',
        'nel', 'nello', 'nella', 'nei', 'negli', 'nelle',
        'sul', 'sullo', 'sulla', 'sui', 'sugli', 'sulle',
    }

    # Add any additional stopwords
    if additional_stopwords:
        stopwords_list = [word.strip() for word in additional_stopwords.split(',')]
        italian_stopwords.update(stopwords_list)

    # Create the word cloud
    wordcloud = WordCloud(
        stopwords=italian_stopwords,
        max_words=max_words,
        width=width,
        height=height,
        background_color='white'
    ).generate(text)

    return wordcloud

def main():
    st.set_page_config(page_title="Word Cloud Generator", layout="wide")

    st.title("Word Cloud Generator")
    st.write("Create a word cloud from your text with custom parameters")

    # File uploader
    uploaded_file = st.file_uploader("Choose a text file", type=['txt'])

    # Text input as alternative
    text_input = st.text_area("Or paste your text here", height=200)

    # Sidebar for parameters
    with st.sidebar:
        st.header("Parameters")

        width = st.number_input("Width", min_value=400, max_value=2000, value=800, step=100)
        height = st.number_input("Height", min_value=200, max_value=1500, value=400, step=100)

        max_words = st.number_input(
            "Maximum number of words",
            min_value=10,
            max_value=500,
            value=200,
            step=10,
            help="Limit the number of words in the cloud"
        )

        additional_stopwords = st.text_input(
            "Additional words to exclude (comma-separated)",
            help="Enter words to exclude, separated by commas"
        )

    if uploaded_file is not None or text_input:
        if st.button("Generate Word Cloud"):
            try:
                # Get text from file or input
                if uploaded_file is not None:
                    text = uploaded_file.getvalue().decode()
                else:
                    text = text_input

                # Generate word cloud
                wordcloud = create_wordcloud(
                    text,
                    additional_stopwords=additional_stopwords,
                    max_words=max_words,
                    width=width,
                    height=height
                )

                # Create plot
                fig, ax = plt.subplots(figsize=(width/100, height/100))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')

                # Display plot
                st.pyplot(fig)

                # Add download button
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
                img_buf.seek(0)
                st.download_button(
                    label="Download Word Cloud",
                    data=img_buf,
                    file_name="wordcloud.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Add instructions and GitHub link
    st.markdown("---")
    st.markdown("""
    ### Instructions
    1. Upload a text file or paste your text directly
    2. Adjust parameters in the sidebar if needed
    3. Click 'Generate Word Cloud'
    4. Download the generated image

    [View source code on GitHub](https://github.com/YOUR_USERNAME/wordcloud-generator)
    """)

if __name__ == "__main__":
    main()
