from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('topics.sqlite', check_same_thread=False)
print("Opened database successfully")



homepage_markup = """
<!DOCTYPE html>
<html>
<head>
<style>

* {{
    box-sizing: border-box;
}}


body {{
  font-family: Arial, Helvetica, sans-serif;
}}

/* Style the header */
.header {{
  grid-area: header;
  background-color: #f1f1f1;
  padding: 30px;
  text-align: center;
  font-size: 35px;
}}

/* The grid container */
.grid-container {{
  display: grid;
  grid-template-areas: 
  'header header header header header header' 
  'left left middle middle right right' 
  'footer footer footer footer footer footer';
  /* grid-column-gap: 10px; - if you want gap between the columns */
}} 

.left,
.middle,
.right {{
  padding: 10px;
  height: 300px; /* Should be removed. Only for demonstration */
}}

/* Style the left column */
.left {{
  grid-area: left;
}}

/* Style the middle column */
.middle {{
  grid-area: middle;
}}

/* Style the right column */
.right {{
  grid-area: right;
}}

/* Style the footer */
.footer {{
  grid-area: footer;
  background-color: #f1f1f1;
  padding: 10px;
  text-align: center;
}}

/* Responsive layout - makes the three columns stack on top of each other instead of next to each other */
@media (max-width: 600px) {{
  .grid-container  {{
    grid-template-areas: 
    'header header header header header header' 
    'left left left left left left' 
    'middle middle middle middle middle middle' 
    'right right right right right right' 
    'footer footer footer footer footer footer';
    }}
}}
</style>
</head>
<body>

<h2>Topics</h2>
<p>Topic Bot

<div class="grid-container">
  <div class="header">
    <h2>Topics</h2>
  </div>
  <div class="left" style="background-color:#aaa;">
    Approved
    {0}
  </div>
  <div class="middle" style="background-color:#bbb;">
    Suggested
    {1}
  </div>  
  <div class="right" style="background-color:#ccc;">
    Removed
    {2}
  </div>
  <div class="footer">
    <p>nan0scho1ar 2018</p>
  </div>
</div>

</body>
</html>
    """





#Create and serve Topic Bot homepage
@app.route('/')
def homepage():
    cursor = conn.execute("SELECT id, TOPIC from APPROVED_TOPICS")
    p1 = ""
    for row in cursor:
        p1 += "<p>{0}: {1}</p>".format(row[0], row[1])
    
    cursor = conn.execute("SELECT id, TOPIC from SUGGESTED_TOPICS")
    p2 = ""
    for row in cursor:
        p2 += "<p>{0}: {1}</p>".format(row[0], row[1])
    return homepage_markup.format(p1, p2, "To be completed")

#_________________________________________________________________________________________________________________________

### T O P I C     A P I ###


### BEGIN APPROVED

# endpoint to create new approved topic
@app.route("/approved", methods=["POST"])
def add_approved():
    TOPIC = request.json['TOPIC']
    CATEGORY = request.json['CATEGORY']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO APPROVED_TOPICS (TOPIC, CATEGORY) VALUES(?,?)''', (TOPIC,CATEGORY))
    conn.commit()
    return jsonify(TOPIC)


# endpoint to show all approved topics
@app.route("/approved", methods=["GET"])
def get_approved():
    cursor = conn.execute("SELECT id, TOPIC, CATEGORY from APPROVED_TOPICS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'TOPIC': row[1], 'CATEGORY': row[2]})
    return jsonify(jdict)


# endpoint to get approved topic detail by id
@app.route("/approved/<id>", methods=["GET"])
def approved_detail(id):
    cursor = conn.execute("SELECT id, TOPIC, CATEGORY from APPROVED_TOPICS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'TOPIC': row[1], 'CATEGORY': row[2]})
    return jsonify(jdict)


# endpoint to update approved topic
@app.route("/approved/<id>", methods=["PUT"])
def approved_update(id):
    TOPIC = request.json['TOPIC']
    CATEGORY = request.json['CATEGORY']
    cursor = conn.execute('''UPDATE APPROVED_TOPICS SET TOPIC = ?, CATEGORY = ?  WHERE id = ? ''', (TOPIC, CATEGORY, id))
    conn.commit()
    return 'OK'


# endpoint to delete approved topic
@app.route("/approved/<id>", methods=["DELETE"])
def approved_delete(id):
    cursor = conn.execute("DELETE from APPROVED_TOPICS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all approved topics
@app.route("/approved", methods=["DELETE"])
def approved_delete_all():
    cursor = conn.execute("DELETE from APPROVED_TOPICS")
    conn.commit()
    return 'OK'


### BEGIN SUGGESTED


# endpoint to create new suggested topic
@app.route("/suggested", methods=["POST"])
def add_suggested():
    TOPIC = request.json['TOPIC']
    CATEGORY = request.json['CATEGORY']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO SUGGESTED_TOPICS (TOPIC, CATEGORY) VALUES(?,?)''', (TOPIC,CATEGORY))
    conn.commit()
    return jsonify(TOPIC)


# endpoint to show all suggested topics
@app.route("/suggested", methods=["GET"])
def get_suggested():
    cursor = conn.execute("SELECT id, TOPIC, CATEGORY from SUGGESTED_TOPICS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'TOPIC': row[1], 'CATEGORY': row[2]})
    return jsonify(jdict)


# endpoint to get suggested topic detail by id
@app.route("/suggested/<id>", methods=["GET"])
def suggested_detail(id):
    cursor = conn.execute("SELECT id, TOPIC, CATEGORY from SUGGESTED_TOPICS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'TOPIC': row[1], 'CATEGORY': row[2]})
    return jsonify(jdict)


# endpoint to update suggested topic
@app.route("/suggested/<id>", methods=["PUT"])
def suggested_update(id):
    TOPIC = request.json['TOPIC']
    CATEGORY = request.json['CATEGORY']
    cursor = conn.execute('''UPDATE SUGGESTED_TOPICS SET TOPIC = ?, CATEGORY = ?  WHERE id = ? ''', (TOPIC, CATEGORY, id))
    conn.commit()
    return 'OK'




# endpoint to delete suggested topic
@app.route("/suggested/<id>", methods=["DELETE"])
def suggested_delete(id):
    cursor = conn.execute("DELETE from SUGGESTED_TOPICS where id=?", (id,))
    conn.commit()
    return 'OK'

# endpoint to delete all suggested topics
@app.route("/suggested", methods=["DELETE"])
def suggested_delete_all():
    cursor = conn.execute("DELETE from SUGGESTED_TOPICS")
    conn.commit()
    return 'OK'













### BEGIN NOMINATIONS

# endpoint to create new nomination
@app.route("/nominations", methods=["POST"])
def add_nominations():
    NOMINATION = request.json['NOMINATION']
    WEIGHT = request.json['WEIGHT']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO NOMINATIONS (NOMINATION, WEIGHT) VALUES(?,?)''', (NOMINATION,WEIGHT))
    conn.commit()
    return jsonify(NOMINATION)


# endpoint to show all nominations
@app.route("/nominations", methods=["GET"])
def get_nominations():
    cursor = conn.execute("SELECT id, NOMINATION, WEIGHT from NOMINATIONS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'NOMINATION': row[1], 'WEIGHT': row[2]})
    return jsonify(jdict)


# endpoint to get nomination by id
@app.route("/nominations/<id>", methods=["GET"])
def nominations_detail(id):
    cursor = conn.execute("SELECT id, NOMINATION, WEIGHT from NOMINATIONS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'NOMINATION': row[1], 'WEIGHT': row[2]})
    return jsonify(jdict)


# endpoint to update nomination
@app.route("/nominations/<id>", methods=["PUT"])
def nominations_update(id):
    NOMINATION = request.json['NOMINATION']
    WEIGHT = request.json['WEIGHT']
    cursor = conn.execute('''UPDATE NOMINATIONS SET NOMINATION = ?, WEIGHT = ?  WHERE id = ? ''', (NOMINATION, WEIGHT, id))
    conn.commit()
    return 'OK'


# endpoint to delete nomination
@app.route("/nominations/<id>", methods=["DELETE"])
def nominations_delete(id):
    cursor = conn.execute("DELETE from NOMINATIONS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all nominations
@app.route("/nominations", methods=["DELETE"])
def nominations_delete_all():
    cursor = conn.execute("DELETE from NOMINATIONS")
    conn.commit()
    return 'OK'


# endpoint to create new nomination
@app.route("/archivednominations", methods=["POST"])
def add_archived_nomination():
    NOMINATION = request.json['NOMINATION']
    WEIGHT = request.json['WEIGHT']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARCHIVEDNOMINATIONS (NOMINATION, WEIGHT) VALUES(?,?)''', (NOMINATION,WEIGHT))
    conn.commit()
    return jsonify(NOMINATION)


# endpoint to show all archivednominations
@app.route("/archivednominations", methods=["GET"])
def get_archived_nomination():
    cursor = conn.execute("SELECT id, NOMINATION, WEIGHT from ARCHIVEDNOMINATIONS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'NOMINATION': row[1], 'WEIGHT': row[2]})
    return jsonify(jdict)


# endpoint to get nomination by id
@app.route("/archivednominations/<id>", methods=["GET"])
def archived_nomination_detail(id):
    cursor = conn.execute("SELECT id, NOMINATION, WEIGHT from ARCHIVEDNOMINATIONS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'NOMINATION': row[1], 'WEIGHT': row[2]})
    return jsonify(jdict)


# endpoint to update nomination
@app.route("/archivednominations/<id>", methods=["PUT"])
def archived_nomination_update(id):
    NOMINATION = request.json['NOMINATION']
    WEIGHT = request.json['WEIGHT']
    cursor = conn.execute('''UPDATE ARCHIVEDNOMINATIONS SET NOMINATION = ?, WEIGHT = ?  WHERE id = ? ''', (NOMINATION, WEIGHT, id))
    conn.commit()
    return 'OK'


# endpoint to delete nomination
@app.route("/archivednominations/<id>", methods=["DELETE"])
def archived_nomination_delete(id):
    cursor = conn.execute("DELETE from ARCHIVEDNOMINATIONS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all archivednominations
@app.route("/archivednominations", methods=["DELETE"])
def archived_nomination_delete_all():
    cursor = conn.execute("DELETE from ARCHIVEDNOMINATIONS")
    conn.commit()
    return 'OK'
















### BEGIN VOTES

# endpoint to create new vote
@app.route("/votes", methods=["POST"])
def add_votes():
    VOTE = request.json['VOTE']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO VOTES (VOTE, DATELODGED) VALUES(?,?)''', (VOTE,DATELODGED))
    conn.commit()
    return jsonify(VOTE)


# endpoint to show all votes
@app.route("/votes", methods=["GET"])
def get_votes():
    cursor = conn.execute("SELECT id, VOTE, DATELODGED from VOTES")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'VOTE': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to get vote by id
@app.route("/votes/<id>", methods=["GET"])
def votes_detail(id):
    cursor = conn.execute("SELECT id, VOTE, DATELODGED from VOTES where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'VOTE': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to update vote
@app.route("/votes/<id>", methods=["PUT"])
def votes_update(id):
    VOTE = request.json['VOTE']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.execute('''UPDATE VOTES SET VOTE = ?, DATELODGED = ?  WHERE id = ? ''', (VOTE, DATELODGED, id))
    conn.commit()
    return 'OK'


# endpoint to delete vote
@app.route("/votes/<id>", methods=["DELETE"])
def votes_delete(id):
    cursor = conn.execute("DELETE from VOTES where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all votes
@app.route("/votes", methods=["DELETE"])
def votes_delete_all():
    cursor = conn.execute("DELETE from VOTES")
    conn.commit()
    return 'OK'


# endpoint to create new vote
@app.route("/archivedvotes", methods=["POST"])
def add_archived_vote():
    VOTE = request.json['VOTE']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARCHIVEDVOTES (VOTE, DATELODGED) VALUES(?,?)''', (VOTE,DATELODGED))
    conn.commit()
    return jsonify(VOTE)


# endpoint to show all archivedvotes
@app.route("/archivedvotes", methods=["GET"])
def get_archived_vote():
    cursor = conn.execute("SELECT id, VOTE, DATELODGED from ARCHIVEDVOTES")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'VOTE': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to get vote by id
@app.route("/archivedvotes/<id>", methods=["GET"])
def archived_vote_detail(id):
    cursor = conn.execute("SELECT id, VOTE, DATELODGED from ARCHIVEDVOTES where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'VOTE': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to update vote
@app.route("/archivedvotes/<id>", methods=["PUT"])
def archived_vote_update(id):
    VOTE = request.json['VOTE']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.execute('''UPDATE ARCHIVEDVOTES SET VOTE = ?, DATELODGED = ?  WHERE id = ? ''', (VOTE, DATELODGED, id))
    conn.commit()
    return 'OK'


# endpoint to delete vote
@app.route("/archivedvotes/<id>", methods=["DELETE"])
def archived_vote_delete(id):
    cursor = conn.execute("DELETE from ARCHIVEDVOTES where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all archivedvotes
@app.route("/archivedvotes", methods=["DELETE"])
def archived_vote_delete_all():
    cursor = conn.execute("DELETE from ARCHIVEDVOTES")
    conn.commit()
    return 'OK'
















### BEGIN COMPLAINTS

# endpoint to create new complaint
@app.route("/complaints", methods=["POST"])
def add_complaints():
    COMPLAINT = request.json['COMPLAINT']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO COMPLAINTS (COMPLAINT, DATELODGED) VALUES(?,?)''', (COMPLAINT,DATELODGED))
    conn.commit()
    return jsonify(COMPLAINT)


# endpoint to show all complaints
@app.route("/complaints", methods=["GET"])
def get_complaints():
    cursor = conn.execute("SELECT id, COMPLAINT, DATELODGED from COMPLAINTS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'COMPLAINT': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to get complaint by id
@app.route("/complaints/<id>", methods=["GET"])
def complaints_detail(id):
    cursor = conn.execute("SELECT id, COMPLAINT, DATELODGED from COMPLAINTS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'COMPLAINT': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to update complaint
@app.route("/complaints/<id>", methods=["PUT"])
def complaints_update(id):
    COMPLAINT = request.json['COMPLAINT']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.execute('''UPDATE COMPLAINTS SET COMPLAINT = ?, DATELODGED = ?  WHERE id = ? ''', (COMPLAINT, DATELODGED, id))
    conn.commit()
    return 'OK'


# endpoint to delete complaint
@app.route("/complaints/<id>", methods=["DELETE"])
def complaints_delete(id):
    cursor = conn.execute("DELETE from COMPLAINTS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all complaints
@app.route("/complaints", methods=["DELETE"])
def complaints_delete_all():
    cursor = conn.execute("DELETE from COMPLAINTS")
    conn.commit()
    return 'OK'


# endpoint to create new complaint
@app.route("/archivedcomplaints", methods=["POST"])
def add_archived_complaint():
    COMPLAINT = request.json['COMPLAINT']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARCHIVEDCOMPLAINTS (COMPLAINT, DATELODGED) VALUES(?,?)''', (COMPLAINT,DATELODGED))
    conn.commit()
    return jsonify(COMPLAINT)


# endpoint to show all archivedcomplaints
@app.route("/archivedcomplaints", methods=["GET"])
def get_archived_complaint():
    cursor = conn.execute("SELECT id, COMPLAINT, DATELODGED from ARCHIVEDCOMPLAINTS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'COMPLAINT': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to get complaint by id
@app.route("/archivedcomplaints/<id>", methods=["GET"])
def archived_complaint_detail(id):
    cursor = conn.execute("SELECT id, COMPLAINT, DATELODGED from ARCHIVEDCOMPLAINTS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'COMPLAINT': row[1], 'DATELODGED': row[2]})
    return jsonify(jdict)


# endpoint to update complaint
@app.route("/archivedcomplaints/<id>", methods=["PUT"])
def archived_complaint_update(id):
    COMPLAINT = request.json['COMPLAINT']
    DATELODGED = request.json['DATELODGED']
    cursor = conn.execute('''UPDATE ARCHIVEDCOMPLAINTS SET COMPLAINT = ?, DATELODGED = ?  WHERE id = ? ''', (COMPLAINT, DATELODGED, id))
    conn.commit()
    return 'OK'


# endpoint to delete complaint
@app.route("/archivedcomplaints/<id>", methods=["DELETE"])
def archived_complaint_delete(id):
    cursor = conn.execute("DELETE from ARCHIVEDCOMPLAINTS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all archivedcomplaints
@app.route("/archivedcomplaints", methods=["DELETE"])
def archived_complaint_delete_all():
    cursor = conn.execute("DELETE from ARCHIVEDCOMPLAINTS")
    conn.commit()
    return 'OK'


### BEGIN ACCOUNTS

# endpoint to create new account
@app.route("/accounts", methods=["POST"])
def add_accounts():
    USERID = request.json['USERID']
    BALANCE = request.json['BALANCE']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ACCOUNTS (USERID, BALANCE) VALUES(?,?)''', (USERID,BALANCE))
    conn.commit()
    return jsonify(USERID)


# endpoint to show all accounts
@app.route("/accounts", methods=["GET"])
def get_accounts():
    cursor = conn.execute("SELECT id, USERID, BALANCE from ACCOUNTS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'BALANCE': row[2]})
    return jsonify(jdict)


# endpoint to get account by id
@app.route("/accounts/<id>", methods=["GET"])
def accounts_detail(id):
    cursor = conn.execute("SELECT id, USERID, BALANCE from ACCOUNTS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'BALANCE': row[2]})
    return jsonify(jdict)


# endpoint to update account
@app.route("/accounts/<id>", methods=["PUT"])
def accounts_update(id):
    USERID = request.json['USERID']
    BALANCE = request.json['BALANCE']
    cursor = conn.execute('''UPDATE ACCOUNTS SET USERID = ?, BALANCE = ?  WHERE id = ? ''', (USERID, BALANCE, id))
    conn.commit()
    return 'OK'


# endpoint to delete account
@app.route("/accounts/<id>", methods=["DELETE"])
def accounts_delete(id):
    cursor = conn.execute("DELETE from ACCOUNTS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all accounts
@app.route("/accounts", methods=["DELETE"])
def accounts_delete_all():
    cursor = conn.execute("DELETE from ACCOUNTS")
    conn.commit()
    return 'OK'


# endpoint to create new account
@app.route("/archivedaccounts", methods=["POST"])
def add_archived_account():
    USERID = request.json['USERID']
    BALANCE = request.json['BALANCE']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARCHIVEDACCOUNTS (USERID, BALANCE) VALUES(?,?)''', (USERID,BALANCE))
    conn.commit()
    return jsonify(USERID)


# endpoint to show all archivedaccounts
@app.route("/archivedaccounts", methods=["GET"])
def get_archived_account():
    cursor = conn.execute("SELECT id, USERID, BALANCE from ARCHIVEDACCOUNTS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'BALANCE': row[2]})
    return jsonify(jdict)


# endpoint to get account by id
@app.route("/archivedaccounts/<id>", methods=["GET"])
def archived_account_detail(id):
    cursor = conn.execute("SELECT id, USERID, BALANCE from ARCHIVEDACCOUNTS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'BALANCE': row[2]})
    return jsonify(jdict)


# endpoint to update account
@app.route("/archivedaccounts/<id>", methods=["PUT"])
def archived_account_update(id):
    USERID = request.json['USERID']
    BALANCE = request.json['BALANCE']
    cursor = conn.execute('''UPDATE ARCHIVEDACCOUNTS SET USERID = ?, BALANCE = ?  WHERE id = ? ''', (USERID, BALANCE, id))
    conn.commit()
    return 'OK'


# endpoint to delete account
@app.route("/archivedaccounts/<id>", methods=["DELETE"])
def archived_account_delete(id):
    cursor = conn.execute("DELETE from ARCHIVEDACCOUNTS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all archivedaccounts
@app.route("/archivedaccounts", methods=["DELETE"])
def archived_account_delete_all():
    cursor = conn.execute("DELETE from ARCHIVEDACCOUNTS")
    conn.commit()
    return 'OK'


### BEGIN ITEMS

# endpoint to create new item
@app.route("/items", methods=["POST"])
def add_items():
    USERID = request.json['USERID']
    ITEM = request.json['ITEM']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ITEMS (USERID, ITEM) VALUES(?,?)''', (USERID,ITEM))
    conn.commit()
    return jsonify(USERID)


# endpoint to show all items
@app.route("/items", methods=["GET"])
def get_items():
    cursor = conn.execute("SELECT id, USERID, ITEM from ITEMS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'ITEM': row[2]})
    return jsonify(jdict)


# endpoint to get item by id
@app.route("/items/<id>", methods=["GET"])
def items_detail(id):
    cursor = conn.execute("SELECT id, USERID, ITEM from ITEMS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'ITEM': row[2]})
    return jsonify(jdict)


# endpoint to update item
@app.route("/items/<id>", methods=["PUT"])
def items_update(id):
    USERID = request.json['USERID']
    ITEM = request.json['ITEM']
    cursor = conn.execute('''UPDATE ITEMS SET USERID = ?, ITEM = ?  WHERE id = ? ''', (USERID, ITEM, id))
    conn.commit()
    return 'OK'


# endpoint to delete item
@app.route("/items/<id>", methods=["DELETE"])
def items_delete(id):
    cursor = conn.execute("DELETE from ITEMS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all items
@app.route("/items", methods=["DELETE"])
def items_delete_all():
    cursor = conn.execute("DELETE from ITEMS")
    conn.commit()
    return 'OK'


# endpoint to create new item
@app.route("/archiveditems", methods=["POST"])
def add_archived_item():
    USERID = request.json['USERID']
    ITEM = request.json['ITEM']
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ARCHIVEDITEMS (USERID, ITEM) VALUES(?,?)''', (USERID,ITEM))
    conn.commit()
    return jsonify(USERID)


# endpoint to show all archiveditems
@app.route("/archiveditems", methods=["GET"])
def get_archived_item():
    cursor = conn.execute("SELECT id, USERID, ITEM from ARCHIVEDITEMS")
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'ITEM': row[2]})
    return jsonify(jdict)


# endpoint to get item by id
@app.route("/archiveditems/<id>", methods=["GET"])
def archived_item_detail(id):
    cursor = conn.execute("SELECT id, USERID, ITEM from ARCHIVEDITEMS where id=?", (id,))
    jdict = []
    for row in cursor:
        jdict.append({'id': row[0],  'USERID': row[1], 'ITEM': row[2]})
    return jsonify(jdict)


# endpoint to update item
@app.route("/archiveditems/<id>", methods=["PUT"])
def archived_item_update(id):
    USERID = request.json['USERID']
    ITEM = request.json['ITEM']
    cursor = conn.execute('''UPDATE ARCHIVEDITEMS SET USERID = ?, ITEM = ?  WHERE id = ? ''', (USERID, ITEM, id))
    conn.commit()
    return 'OK'


# endpoint to delete item
@app.route("/archiveditems/<id>", methods=["DELETE"])
def archived_item_delete(id):
    cursor = conn.execute("DELETE from ARCHIVEDITEMS where id=?", (id,))
    conn.commit()
    return 'OK'


# endpoint to delete all archiveditems
@app.route("/archiveditems", methods=["DELETE"])
def archived_item_delete_all():
    cursor = conn.execute("DELETE from ARCHIVEDITEMS")
    conn.commit()
    return 'OK'

if __name__ == '__main__':
    app.run(debug=False)
