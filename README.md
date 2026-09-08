# ShelfLight

A Python desktop application to address a grid of LEDs through a Raspberry Pi. 

# Features
- Manual LED control
- Screen reflection
- Desktop GUI

# Architecture
The desktop application communicates to the Raspberry Pi using a WebSocket connection. Commands are serialized as JSON containing a lighting mode and its associated data.

# Tech Stack
Languages
- Python
  
Frameworks and Libraries:
- PySide6
- NumPy
- Pillow
- MSS
- websocket-client

# Installation
1. Clone the repository with 'git clone https://github.com/AA-1nc/shelf-light.git' and 'cd shelf-light'
2. Install the required packages with 'pip install PySide6 numpy Pillow mss websocket-client'
3. Configure the Raspberry Pi's WebSocket address in network.py
4. Start the application with 'python app.py'

# Future Improvements
- Automatic device discovery
- Improved connection management
- Additional lighting modes and effects
- Improved configuration and setup experience

# License
This project is currently intended as a personal project. No license has been specified yet. 
