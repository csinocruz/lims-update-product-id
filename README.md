# lims-update-product-id
Update ProductID udf attached to submitted samples in the VSeq and Exome+ workflows. 

## Usage
The script takes the LIMS username and password, Root URI for the API, File Name, and the new ProductID parameters as command-line arguments.
```sh
python3 update_product_id.py -u {username} -p {password} -r {root_uri} -f {file_name or file_path} -pi {product_id}
```
Example:
```sh
python3 update_product_id.py -u {username} -p {password} -r https://test.lims.lusk.helix.net/api/v2 -f test_lusk_samples_01.csv -pi 99999_22222_22222_11111
```
### CSV File
The script takes the list of samples from a csv file. The csv should not contain a header. Each row should contain a single sample and all samples should be within the first column. 

> Note: As suggested by Semaphore, the list will be split into groups of `96 samples` because the `query()` and `batch_update()` operations can fail with too large a number of samples.
## Errors
You may come across:
```sh
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

By default SSL validation is disabled, but for some reason it still attempts to validate. 
```sh
class s4.clarity.LIMS(root_uri, username, password, dry_run=False, insecure=False, log_requests=False, timeout=None)
```
> insecure (bool) – Disables SSL validation. Default false.

To get get around this, you may need to temporarily modify the Python Requests library. I needed to modify this file: `/usr/local/lib/python3.9/site-packages/requests/sessions.py`
sessions.py: 
```sh
#: SSL Verification default.
#: Defaults to `True`, requiring requests to verify the TLS certificate at the
#: remote end.
#: If verify is set to `False`, requests will accept any TLS certificate
#: presented by the server, and will ignore hostname mismatches and/or
#: expired certificates, which will make your application vulnerable to
#: man-in-the-middle (MitM) attacks.
#: Only set this to `False` for testing.
self.verify = True
```
Setting `self.verify = False` and re-run the script.

## Reference
- [S4-Clarity Library] - The S4-Clarity library lets developers interact with the Clarity API
-  [Clarity API] - The REST Data Access Web Service is the fundamental interface in the GenoLogics Rapid Scripting API.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [S4-Clarity Library]: <https://s4-clarity-lib.readthedocs.io/en/stable/>
   [Clarity API]: <https://d10e8rzir0haj8.cloudfront.net/4.2/REST.html>
   

