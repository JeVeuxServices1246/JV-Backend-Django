
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_email(data):
    response_data = {'status': False, 'message': 'Something went wrong'}
    try:
        name = data.get('name', 'user')
        email = data.get('email')
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        subject = 'Invitation to JV Services'
        sender = {"name": 'jvs', "email": 's.sirajuddin@ez-xpert.ca'}
        to = [{"email": email, "name": name}]
        headers = {"welcome": "unique-id-1234"}

        # attachments = [
        #     {"url": "https://www.africau.edu/images/default/sample.pdf", "name": "attachment1.pdf"},
        # ]
        # , attachment=attachments,
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, template_id=1, params={
            'name': name
        }, sender=sender, subject=subject)
            
        api_response = api_instance.send_transac_email(send_smtp_email)

        if api_instance:
            response_data['status'] = True
            response_data['message'] = 'Mail sent'
        else:
            response_data['message'] = 'Error Sending mail'
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}")
    return response_data