import smtplib
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from services.dataverse.dataset.metadata import get_dataset_contact
from utils.logging import logging
from typing import List, Optional
from utils.generic import async_id_from_args
from services import note, history
from services.dataverse import user
from services.dataverse.dataset import metadata

RDM_HELPDESK_EMAILS = []
TEST_EMAIL = ""
SMTP_HOST = ""
SMTP_PORT = ""
SMTP_PASSWORD = ""
DATAVERSE_URL = ""


async def send_email(
    from_: str,
    to: List[str],
    subject: str,
    text: str,
    server: str,
    port: int,
    files: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    html: str = None,
    username=None,
    password=None,
    use_tls=False,
):
    """Sends an email with the specified settings. If a test email address has been set in the settings.json, the email will be sent from that address."""

    if TEST_EMAIL:
        logging.info(
            f"Test Email address set: Emails will be sent to {TEST_EMAIL} instead of {to}."
        )
        to = TEST_EMAIL

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_
    message["To"] = COMMASPACE.join(to)
    message["Date"] = formatdate(localtime=True)

    if cc:
        message["CC"] = ", ".join(to)
    if bcc:
        message["BCC"] = ", ".join(to)

    mime_text = MIMEText(text, "plain")
    message.attach(mime_text)

    if html:
        mime_html = MIMEText(html, "html")
        message.attach(mime_html)

    for path in files or []:
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename={}".format(Path(path).name)
        )
        message.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:

            if use_tls:
                smtp.starttls()

            smtp.ehlo()
            if username is not None and password is not None:
                smtp.login(username, password)

            result = smtp.sendmail(from_, to, message.as_string())
            logging.info(
                f"Email sent: \n host: {SMTP_HOST}, \n port: {SMTP_PORT}, \n subject: {subject}, \n from: {from_}, to: {to}"
            )
            smtp.quit()

    except Exception as e:
        logging.error(
            f"Sending email failed: {server}, {port}, {from_}, {to}, {subject} \n{e}"
        )
        result = False

    return result


async def send_feedback_email(persistent_identifier: str, logged_user: str):
    """Sends the stored feedback email to the dataset contributor."""
    note_id = await async_id_from_args(persistent_identifier)
    email_text = note.get_note_by_id(persistent_identifier, note_id, "feedback").get(
        "text", ""
    )

    email_html = email_text.replace("\n", "</br>")

    dataset_contact_info = await get_dataset_contact(persistent_identifier)
    email_address = [contact.get("datasetContactEmail") for contact in dataset_contact_info]
    cc = []

    if len(email_address) == 0:
        logging.warning(
            f"Feedback email could not be sen for {persistent_identifier}: No contributor email!"
        )
        return False

    logged_user_details = await user.get_user_info(logged_user)
    logged_user_name = logged_user_details.get("name", logged_user)
    email_subject = f"Dataset feedback from review [Reviewed by {logged_user_name}]"

    result = False
    if email_address or TEST_EMAIL:
        if SMTP_HOST and SMTP_PORT and RDM_HELPDESK_EMAILS:
            result = await send_email(
                TEST_EMAIL or RDM_HELPDESK_EMAILS[0],
                TEST_EMAIL or email_address,
                email_subject,
                email_text,
                SMTP_HOST,
                SMTP_PORT,
                html=email_html,
                cc=TEST_EMAIL or cc,
            )
        else:
            result = False
            logging.error(
                f"Feedback email to {email_address} for {persistent_identifier} could not be sent. Server not configured."
            )

        if result:
            history_update = f"Feedback email sent contributor by {logged_user}."
            tags = [
                {"type": "category", "content": "Email"},
                {"type": "subcategory", "content": "Feedback"},
            ]

            history.append_to_history(
                persistent_identifier, history_update, user_id=logged_user, tags=tags
            )
            logging.info(
                f"Feedback email sent to {email_address} for {persistent_identifier}"
            )
        else:
            logging.error(
                f"Feedback email could not be sent to {email_address} for {persistent_identifier}"
            )

    return result


async def send_support_requested_email(
    persistent_identifier: str, logged_user: str, remove: bool = False
):
    """Sends an email to the helpdesk indicating that the user has requested support."""
    dataset_ = await metadata.async_get_dataset_details(persistent_identifier)
    logged_user_details = await user.get_user_info(logged_user)
    logged_user_name = logged_user_details.get("name", logged_user)
    if not remove:
        email_subject = f"Support requested for dataset [{persistent_identifier}] by [{logged_user_name}]."
        email_text = f"Support requested for dataset {persistent_identifier} by {logged_user_name}."
    else:
        email_subject = f"Support request removed for dataset [{persistent_identifier}] by [{logged_user_name}]."
        email_text = f"Support request removed for dataset {persistent_identifier} by {logged_user_name}."

    email_text += "\n\n"

    note_id = await async_id_from_args(persistent_identifier)
    _note = note.get_note_by_id(persistent_identifier, note_id, "note")
    email_text += f'Internal review notes for the dataset ({_note.get("modified")}):\n'

    email_text += _note.get("text", "--no notes--")
    email_html = email_text.replace("\n", "</br>")
    url = f"{DATAVERSE_URL}/dataset.xhtml?persistentId={persistent_identifier}"
    if (
        dataset_
        and dataset_.get("versionstate") == "DRAFT"
        or dataset_.get("versionstate") == "in_review"
    ):
        url += "&version=DRAFT"
    email_text += f"\nDataset URL: {url}"
    email_html += f'<br> <a href="{url}">{url}</a>'
    if SMTP_HOST and SMTP_PORT and RDM_HELPDESK_EMAILS:
        result = await send_email(
            TEST_EMAIL or RDM_HELPDESK_EMAILS[0],
            TEST_EMAIL or RDM_HELPDESK_EMAILS,
            email_subject,
            email_text,
            SMTP_HOST,
            SMTP_PORT,
        )
    else:
        logging.error(f"Email could not be sent: settings missing")
        result = False

    return result
