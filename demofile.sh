
mkdir templates 
python3 scaffold.py liste_courses_nourriture date name
python3 scaffold.py list_item liste_courses_nourriture_id:references item_name
python3 scaffold.py user username phone email password country_id:references
python3 scaffold.py country name
python3 scaffold.py bedroom name
python3 scaffold.py musicgenre name
python3 scaffold.py usersharemusicstyle user_id:references musicgenre_id:references
python3 scaffold.py usersharebed bedroom_id:references user_id:references
