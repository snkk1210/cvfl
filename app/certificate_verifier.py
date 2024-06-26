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
        try:
            with open(self.cert_file_path, "rb") as file:
                cert_data = file.read()

            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            public_key = cert.public_key()

            modulus = public_key.public_numbers().n
            md5_hash = hashlib.md5(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).hexdigest()

            return md5_hash
        except FileNotFoundError:
            return "ERROR: Certificate file not found."
        except ValueError as e:
            return f"ERROR: Unable to load PEM file. {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred. {e}"
    
    def get_rsa_modulus_md5(self):
        try:
            with open(self.privkey_file_path, "rb") as file:
                key_data = file.read()

            private_key = serialization.load_pem_private_key(
                key_data,
                password=None,
            )

            modulus = private_key.private_numbers().public_numbers.n
            md5_hash = hashlib.md5(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).hexdigest()

            return md5_hash
        except FileNotFoundError:
            return "ERROR: Private key file not found."
        except ValueError as e:
            return f"ERROR: Unable to load PEM file. {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred. {e}"

    def get_certificate_issuer_cn(self):
        try:
            with open(self.cert_file_path, "rb") as file:
                cert_data = file.read()

            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            issuer = cert.issuer
            cn = issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

            return cn
        except FileNotFoundError:
            return "ERROR: Certificate file not found."
        except ValueError as e:
            return f"ERROR: Unable to load PEM file. {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred. {e}"

    def get_certificate_subject_cn(self):
        try:
            with open(self.chain_file_path, "rb") as file:
                cert_data = file.read()

            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            subject = cert.subject
            cn = subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

            return cn
        except FileNotFoundError:
            return "ERROR: Chain file not found."
        except ValueError as e:
            return f"ERROR: Unable to load PEM file. {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred. {e}"
    
    def get_certificate_dates(self):
        try:
            with open(self.cert_file_path, "rb") as file:
                cert_data = file.read()

            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            not_before = cert.not_valid_before_utc
            not_after = cert.not_valid_after_utc

            return str(not_before) + " - " + str(not_after)
        except FileNotFoundError:
            return "ERROR: Certificate file not found."
        except ValueError as e:
            return f"ERROR: Unable to load PEM file. {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred. {e}"
    
    def verify_certificate_integrity(self):
        for method_name in ["get_certificate_modulus_md5", "get_rsa_modulus_md5",
                            "get_certificate_issuer_cn", "get_certificate_subject_cn",
                            "get_certificate_dates"]:
            result = getattr(self, method_name)()
            if isinstance(result, str) and result.startswith("ERROR"):
                return result

        if self.get_certificate_modulus_md5() == self.get_rsa_modulus_md5():
            if self.get_certificate_issuer_cn() == self.get_certificate_subject_cn():
                return self.get_certificate_dates()
            else:
                return "ERROR: The issuer of the certificate does not match the CA subject."
        else:
            return "ERROR: The modulus hash of the certificate does not match the modulus hash of the private key."