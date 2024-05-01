from IPython.display import HTML, display

def plt_img_base64(img_base64):
    # Create an HTML img tag with the base64 string as the source
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'

    # Display the image by rendering the HTML
    display(HTML(image_html))

def runRAG(chain):
    docs = retriever.get_relevant_documents("Woman with children", k=10)
    for doc in docs:
        if is_base64(doc.page_content):
            plt_img_base64(doc.page_content)
        else:
            print(doc.page_content)

    chain.invoke("Woman with children")