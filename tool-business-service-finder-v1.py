import streamlit as st
import requests
import json

# Function to call the Gemini API
def call_gemini_api(query, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": query}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        # Extract the generated content from the response
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch response from API. Details: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from API."

# Streamlit app
def main():
    # Set page configuration
    st.set_page_config(page_title="Finder App", page_icon="🔍", layout="wide")

    # Title and description
    st.title("🔍 Tool, Business, and Service Finder")
    st.markdown("""
    Welcome to the Finder App! Use this tool to search for tools, businesses, or services. 
    Simply select a category, enter your query, and get detailed results powered by AI.
    """)

    # API Key input (in real apps, store this securely, e.g., in environment variables)
    api_key = st.text_input("Enter your Gemini API Key", type="password", value="YOUR_API_KEY_HERE")
    
    # Category selection
    category = st.selectbox(
        "Select a Category",
        ["Tool Finder", "Business Finder", "Service Finder"]
    )

    # Query input
    query = st.text_area("Enter your query", placeholder="e.g., 'Find a tool for project management' or 'Locate a business for web design'")

    # Button to submit query
    if st.button("Search"):
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            st.error("Please provide a valid Gemini API Key.")
        elif not query.strip():
            st.error("Please enter a query.")
        else:
            with st.spinner("Searching..."):
                # Customize the prompt based on the selected category
                if category == "Tool Finder":
                    full_query = f"Find and describe tools that can help with: {query}. Provide names, features, and where to find them."
                elif category == "Business Finder":
                    full_query = f"Locate businesses that offer: {query}. Include business names, locations, and contact details if possible."
                else:  # Service Finder
                    full_query = f"Identify services related to: {query}. List service providers, descriptions, and how to access them."

                # Call the API
                result = call_gemini_api(full_query, api_key)

                # Display the result
                st.subheader("Results")
                if result.startswith("Error:"):
                    st.error(result)
                else:
                    st.write(result)

    # Footer
    st.markdown("""
    ---
    *Powered by Google Gemini API | Built with Streamlit | Date: April 09, 2025*
    """)

if __name__ == "__main__":
    main()
