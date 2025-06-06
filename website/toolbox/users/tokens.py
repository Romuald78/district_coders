from django.contrib.auth.tokens import PasswordResetTokenGenerator
import hashlib

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        h = hashlib.sha3_256()
        h.update((user.pk).to_bytes(8, byteorder='big'))
        h.update((timestamp).to_bytes(8, byteorder='big'))
        out = h.digest()
        return out

account_activation_token = AccountActivationTokenGenerator()