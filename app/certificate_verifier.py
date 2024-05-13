from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
import hashlib

class CertificateVerifier:
    def __init__(self, cert_file_path, privkey_file_path, chain_file_path):
        self.cert_file_path = cert_file_path
        self.privkey_file_path = privkey_file_path
        self.chain_file_path = chain_file_path

    def get_certificate_modulus_md5(self):
        with open(self.cert_file_path, "rb") as file:
            cert_data = file.read()

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        public_key = cert.public_key()

        modulus = public_key.public_numbers().n
        md5_hash = hashlib.md5(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).hexdigest()

        return md5_hash
    
    def get_rsa_modulus_md5(self):
        with open(self.privkey_file_path, "rb") as file:
            key_data = file.read()

        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
        )

        modulus = private_key.private_numbers().public_numbers.n
        md5_hash = hashlib.md5(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).hexdigest()

        return md5_hash

    def get_certificate_issuer_cn(self):
        with open(self.cert_file_path, "rb") as file:
            cert_data = file.read()

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        issuer = cert.issuer
        cn = issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        return cn

    def get_certificate_subject_cn(self):
        with open(self.chain_file_path, "rb") as file:
            cert_data = file.read()

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        subject = cert.subject
        cn = subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

        return cn
    
    def get_certificate_dates(self):
        with open(self.cert_file_path, "rb") as file:
            cert_data = file.read()

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        not_before = cert.not_valid_before_utc
        not_after = cert.not_valid_after_utc

        return str(not_before) + " - " + str(not_after)
    
    def verify_certificate_integrity(self):
        cert_modulus_hash = self.get_certificate_modulus_md5()
        key_modulus_hash = self.get_rsa_modulus_md5()
        cert_issuer_cn = self.get_certificate_issuer_cn()
        ca_subject_cn = self.get_certificate_subject_cn()
        cert_dates = self.get_certificate_dates()

        if cert_modulus_hash == key_modulus_hash:
            if cert_issuer_cn == ca_subject_cn:
                return cert_dates
            else:
                return "NG: CERT_ISSUER_CN and CA_SUBJECT_CN"
        else:
            return "NG: CERT_HASH and KEY_HASH"



