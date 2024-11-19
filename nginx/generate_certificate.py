#!../.venv/bin/python3
from OpenSSL import crypto


def cert_gen():
    email_address = "dummy@fruitpassion.fr"
    common_name = "localhost"
    country_name = "FR"
    locality_name = "France"
    state_name = "Toulouse"
    organization_name = "Apeaj"
    organization_unit_name = "Dev"
    serial_number = 0
    validity_start = 0
    validity_end = 10 * 365 * 24 * 60 * 60
    KEY_FILE = "./ssl/private/self_ssl_certs.key"
    CERT_FILE = "./ssl/certs/self_ssl_certs.pem"

    # Generate the private key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # Create a self-signed certificate
    cert = crypto.X509()
    cert.get_subject().C = country_name
    cert.get_subject().ST = state_name
    cert.get_subject().L = locality_name
    cert.get_subject().O = organization_name
    cert.get_subject().OU = organization_unit_name
    cert.get_subject().CN = common_name
    cert.get_subject().emailAddress = email_address
    cert.set_serial_number(serial_number)
    cert.gmtime_adj_notBefore(validity_start)
    cert.gmtime_adj_notAfter(validity_end)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, "sha512")

    # Write the private key to a PEM file
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

    # Write the certificate to a PEM file
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))


# Call the function to generate the key and certificate
cert_gen()
