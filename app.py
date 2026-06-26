from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

#GET methods
@app.route('/', methods=["GET"])
def home():
    return jsonify({"message":"Welcome!"}), 200

@app.route('/events', methods=["GET"])
def get_events():
    return (jsonify([event.to_dict()for event in events]), 200)

@app.route('/events/<int:event_id>', methods=["GET"])
def get_event(id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error":"Event not found"}), 404
    return jsonify(event.to_dict()), 200


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error":"Title required"}), 400
    
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201
    

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data= request.get_json()
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error":"Event not found"}), 404
    
    if "title" in data:
        event.title = data["title"]
    return jsonify(event.to_dict()), 200
    

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error":"Event not found"}), 404
    events = [e for e in events != event_id ]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
