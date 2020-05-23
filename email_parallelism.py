@event.route("/event/send/<eventid>")
def send_ticket(eventid):
    # Query event
    event = Event.query.filter(Event.id == eventid).first()

    # get the audience relationship
    audiences = event.audience

    # if there is no audience uploaded response 404
    if not audiences:
        return jsonify({"sent": None}), 404

    # create the list and some variables for send_email func kwargs
    audience_list_object = []
    subject = f"Digital Ticket from {event.name} Event"
    msg = event.body

    # load the Audience object and append to the list
    for people in audiences:
        identity = people.id
        email = people.email
        audience_list_object.append(AudienceEmail(identity, email))

    # Parallelism sending email
    email_arguments = {"audiences": audience_list_object, "subject": subject, "message": msg}
    email_parallel = Thread(target=send_email, kwargs=email_arguments)

    # Start the parallelism
    email_parallel.start()
    
    return jsonify({"sent": True})
