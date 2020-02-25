import logging

from haystack import indexes

from api.v2.models.Credential import Credential as CredentialModel
from api.v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class CredentialIndex(TxnAwareSearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True)

    topic_source_id = indexes.CharField(model_attr="source_id")
    topic_type = indexes.CharField(model_attr="type")
    topic_all_credentials_inactive = indexes.BooleanField()
    topic_all_credentials_revoked = indexes.BooleanField()

    def get_model(self):
        return CredentialModel

    @staticmethod
    def prepare_topic_all_credentials_inactive(obj):
        all_creds_inactive = True
        for credential in obj.credentials.all():
            if not credential.inactive:
                all_creds_inactive = False
        return all_creds_inactive

    @staticmethod
    def prepare_name_credential_revoked(obj):
        all_creds_revoked = True
        for credential in obj.credentials.all():
            if not credential.revoked:
                all_creds_revoked = False
        return all_creds_revoked