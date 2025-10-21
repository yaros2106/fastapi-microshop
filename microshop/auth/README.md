# Issue RSA private key + public key pair

```shell
# Generate an RSA private key, of size 2048
openssl genpkey -algorithm Ed25519 -out jwt-private.pem
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl pkey -in jwt-private.pem -pubout -out jwt-public.pem
```