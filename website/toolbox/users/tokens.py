from django.contrib.auth.tokens import PasswordResetTokenGenerator
import hashlib

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        h = hashlib.sha3_256()
        h.update(user.pk)
        h.update(timestamp)
        h.update(user.is_email_validated)
        out = h.digest()
        return out

account_activation_token = AccountActivationTokenGenerator()