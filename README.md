# lims-update-product-id
Update ProductID's for samples in the VSeq and Exome+ workflow.

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

> Note: `.` .
## Reference
- [S4-Clarity Library] - The S4-Clarity library lets developers interact with the Clarity API
-  [Clarity API] - The REST Data Access Web Service is the fundamental interface in the GenoLogics Rapid Scripting API.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [S4-Clarity Library]: <https://s4-clarity-lib.readthedocs.io/en/stable/>
   [Clarity API]: <https://d10e8rzir0haj8.cloudfront.net/4.2/REST.html>
   

