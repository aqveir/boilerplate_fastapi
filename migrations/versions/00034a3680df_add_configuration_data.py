"""Add configuration data

Revision ID: 00034a3680df
Revises: 33ae8db5d28c
Create Date: 2025-05-24 00:22:23.949402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00034a3680df'
down_revision: Union[str, None] = '33ae8db5d28c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    configuration_table = sa.sql.table(
        'configurations',
        sa.sql.column('data_key', sa.String),
        sa.sql.column('display_name', sa.String),
        sa.sql.column('data_type', sa.String),
        sa.sql.column('data_schema', sa.String),
        sa.sql.column('filter', sa.String),
        sa.sql.column('default_value', sa.String),
        sa.sql.column('allow_multiple', sa.Boolean),
    )

    op.bulk_insert(
        configuration_table,
        [
            {
                'data_key': 'configuration_mail_smtp',
                'display_name': 'Mail SMTP Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"mail_host": "smtp.mailtrap.io", "mail_port": 2525, "mail_username": "username", "mail_password": "password", "mail_encrypt": null, "mail_from_address": "john@doe.com", "mail_from_name": "John Doe"}',
                'filter': None,
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_call_providers',
                'display_name': 'Telephony Call Providers',
                'data_type': 'data_type_lookup',
                'data_schema': '[{"provider_key":"configuration_telephony_providers_none","display_value":"None"},{"provider_key":"configuration_telephony_providers_exotel","display_value":"Exotel India"},{"provider_key":"configuration_telephony_providers_knowlarity","display_value":"Knowlarity India"},{"provider_key":"configuration_telephony_providers_servetel","display_value":"Servetel India"},{"provider_key":"configuration_telephony_providers_twilio","display_value":"Twilio"}]',
                'filter': None,
                'default_value': 'configuration_telephony_providers_none',
                'allow_multiple': True
            },
            {
                'data_key': 'configuration_telephony_call_exotel',
                'display_name': 'Exotel Call Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"exotel_subdomain":"exotel_subdomain","exotel_sid":"enter_exotel_sid","exotel_api_key":"enter_exotel_api_key","exotel_api_token":"enter_exotel_api_token", "exotel_from_number": "your_exotel_from_number"}',
                'filter': 'configuration_telephony_call_providers_exotel',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_call_knowlarity',
                'display_name': 'Knowlarity Call Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"knowlarity_sid": "your_knowlarity_sid", "knowlarity_token": "your_knowlarity_token", "knowlarity_from_number": "your_knowlarity_from_number"}',
                'filter': 'configuration_telephony_call_providers_knowlarity',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_call_servetel',
                'display_name': 'Servetel Call Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"servetel_sid": "your_servetel_sid", "servetel_token": "your_servetel_token", "servetel_from_number": "your_servetel_from_number"}',
                'filter': 'configuration_telephony_call_providers_servetel',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_call_twilio',
                'display_name': 'Twilio Call Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"twilio_base_url":"enter_twilio_base_url", "twilio_account_sid": "your_twilio_account_sid", "twilio_api_key":"enter_twilio_api_key", "twilio_auth_token": "your_twilio_auth_token", "twilio_from_number": "your_twilio_from_number"}',
                'filter': 'configuration_telephony_call_providers_twilio',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_sms_providers',
                'display_name': 'Telephony SMS Providers',
                'data_type': 'data_type_lookup',
                'data_schema': '[{"provider_key":"configuration_telephony_sms_providers_none","display_value":"None"},{"provider_key":"configuration_telephony_sms_providers_exotel","display_value":"Exotel"}, {"provider_key":"configuration_telephony_sms_providers_twilio","display_value":"Twilio"},{"provider_key":"configuration_telephony_sms_providers_indiasms","display_value":"India SMS"}, {"provider_key":"configuration_telephony_sms_providers_2","display_value":"Provider 2"}]',
                'filter': None,
                'default_value': 'configuration_telephony_providers_none',
                'allow_multiple': True
            },
            {
                'data_key': 'configuration_telephony_sms_exotel',
                'display_name': 'Exotel SMS Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"exotel_subdomain":"exotel_subdomain","exotel_sid":"enter_exotel_sid","exotel_api_key":"enter_exotel_api_key","exotel_api_token":"enter_exotel_api_token", "exotel_from_number": "your_exotel_from_number"}',
                'filter': 'configuration_telephony_sms_providers_exotel',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_sms_twilio',
                'display_name': 'Twilio SMS Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"twilio_base_url":"enter_twilio_base_url", "twilio_account_sid": "your_twilio_account_sid", "twilio_api_key":"enter_twilio_api_key", "twilio_auth_token": "your_twilio_auth_token", "twilio_from_number": "your_twilio_from_number"}',
                'filter': 'configuration_telephony_sms_providers_twilio',
                'default_value': None,
                'allow_multiple': False
            },
            {
                'data_key': 'configuration_telephony_sms_indiasms',
                'display_name': 'India SMS Provider Configuration',
                'data_type': 'data_type_json',
                'data_schema': '{"api_endpoint":"api_endpoint_url","api_username":"api_username","api_password ":"api_password","api_verb":"GET","sms_type":"TEXT","sender":"your-6char-senderid","payload_signature":{"username":"[api_username]","password":"[api_password]","type":"[sms_type]","sender":"[sender]","mobile":"[!mobile_number!]","message":"[!sms_message!]"}}',
                'filter': 'configuration_telephony_sms_providers_indiasms',
                'default_value': '{"api_endpoint":"https://app.indiasms.com/sendsms/bulksms.php","api_username":"api_username","api_password ":"api_password","api_verb":"GET","sms_type":"TEXT","sender":"your-6char-senderid","payload_signature":{"username":"[api_username]","password":"[api_password]","type":"[sms_type]","sender":"[sender]","mobile":"[!mobile_number!]","message":"[!sms_message!]"}}',
                'allow_multiple': False
            }
        ],
        multiinsert=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Truncate the configurations table
    # op.execute("TRUNCATE TABLE configurations")
    pass
