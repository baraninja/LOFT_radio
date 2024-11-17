import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="LOFT Podcast Player",
    page_icon="🎧",
    layout="wide"
)

def parse_rss_feed(url="https://partnerskapetloft.se/feed/podcast/"):
    """Fetch and parse the RSS feed"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        channel = root.find('channel')
        
        # Extract episodes
        episodes = []
        for item in channel.findall('item'):
            episode = {
                'title': item.find('title').text,
                'description': item.find('description').text,
                'publication_date': datetime.strptime(
                    item.find('pubDate').text, 
                    '%a, %d %b %Y %H:%M:%S %z'
                ).strftime('%Y-%m-%d'),
                'duration': item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text,
                'audio_url': item.find('enclosure').attrib['url']
            }
            episodes.append(episode)
        
        return episodes
    except Exception as e:
        st.error(f"Error fetching podcast feed: {str(e)}")
        return []

def main():
    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        footer {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        .element-container:has(button) {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Header
    st.title("🎧 LOFT Podcast Player")
    st.markdown("*En podd om förnyelse och transformation*")
    
    # Fetch episodes
    episodes = parse_rss_feed()
    
    if episodes:
        # Display episodes
        for episode in episodes:
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(episode['title'])
                st.markdown(f"*Publicerad: {episode['publication_date']} • Längd: {episode['duration']}*")
                with st.expander("Visa beskrivning"):
                    st.markdown(episode['description'])
            
            with col2:
                st.audio(episode['audio_url'])
    else:
        st.warning("Kunde inte ladda podcastavsnitt. Försök igen senare.")
    
    # Footer
    st.markdown("""
        <div style='position: fixed; bottom: 0; right: 0; padding: 1rem;'>
        Developed by Anders Barane
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
