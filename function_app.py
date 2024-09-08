import logging as logger
import os
import requests
import azure.functions as func

app = func.FunctionApp()


@app.route(route="mail", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.ANONYMOUS)
def mail_sender(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        email = req_body.get('email')
        message = req_body.get('message')
    except ValueError:
        return func.HttpResponse(
            "Invalid input. Make sure to provide 'name', 'email', and 'message'.",
            status_code=400
        )

    brevo_api_key = os.getenv("BREVO_API_KEY")
    brevo_url = "https://api.brevo.com/v3/smtp/email"

    # Email content
    email_data = {
        "sender": {
            "name": "Gianluigi De Marco",
            "email": "dem.gianluigi@gmail.com"
        },
        "to": [
            {
                "name": "Gianluigi De Marco",
                "email": "dem.gianluigi@gmail.com"
            }
        ],
        "subject": "Message from your portfolio's contact form",
        "htmlContent": f"<html><head></head><body><p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong> {message}</p></body></html>"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": brevo_api_key
    }

    response = requests.post(brevo_url, json=email_data, headers=headers)

    if response.status_code == 201:
        return func.HttpResponse(f"Email successfully sent.", status_code=201)
    else:
        logger.log(20, f"Error sending the mail: {response.text}")
        return func.HttpResponse(f"Failed to send email.", status_code=500)
