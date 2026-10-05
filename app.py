import streamlit as st
import os
import tempfile

from shopping_agent import agent

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒"
)

st.title("🛒 AI Shopping Assistant")
st.caption(
    "Tell me what you want – I'll search, rate, and order the best match for you."
)

# ---------------------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_image" not in st.session_state:
    st.session_state.pending_image = None


# ---------------------------------------------------------------------------------------
# Sidebar - Shop by image
# ---------------------------------------------------------------------------------------

with st.sidebar:
    st.header("Shop by Image")
    st.caption(
        "Upload a photo of a product and I'll find similar items in our store."
    )

    uploaded_file = st.file_uploader(
        "Upload product image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            use_container_width=True
        )

    if uploaded_file and st.button(
        "Find similar products",
        use_container_width=True
    ):

        suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:
            tmp.write(uploaded_file.getvalue())
            image_path = tmp.name

        prompt = (
            f"I uploaded a product image. "
            f"Please analyze it and find similar products. "
            f"The image is located at: {image_path}"
        )

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        st.session_state.pending_image = image_path

        st.rerun()


# ---------------------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(
            msg["content"].replace("$", r"\$")
        )

prompt = st.chat_input(
    "e.g. I want organic honey under $15 with 4+ rating"
)

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

if st.session_state.pending_image:

    with st.chat_message("assistant"):
        with st.spinner("Analyzing image and finding similar products..."):

            result = agent.invoke({
                "messages": st.session_state.messages
            })

            response = result["messages"][-1].content

            st.markdown(
                response.replace("$", r"\$")
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.pending_image = None

    st.rerun()

elif prompt:

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            result = agent.invoke({
                "messages": st.session_state.messages
            })

            response = result["messages"][-1].content

            st.markdown(
                response.replace("$", r"\$")
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()