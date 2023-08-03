# liu-group-database-website
# This is the repository for the Liu Group website to visualize a research database. 
# Access current plans on this Google Doc at https://docs.google.com/document/d/18N7HasQ_jVM7JYmAk5Ua3-3R2ZhmTneQYEx8KQuaTw4/edit?usp=sharing.


# Activate the script virtual environment
source venv/bin/activate         
# Run the flask script
python3 app.py
# Deactivate the script virtual environment
deactivate

# Start backend
node connect_to_db.js
# Start frontend
open index.html