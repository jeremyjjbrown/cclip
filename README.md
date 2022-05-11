# cclip
Simple cloud-backed, shared clipboard with clinet side AES

## Getting Started

### Prequisites
1. Install Python

    ```
    brew install python3
    ```
2. Install `gnupg` if not Already
    ```
    brew install gnupg
    ```
4. Clone this repository
5. Configure AWS Credentials
    1. [Create AWS IAM User and get Access Keypair](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html)
    2. [Create a Named AWS Profile on your Machine](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-profiles)

### Install cclip
  ```
  pip3 install [path-to-cclip-repo]
  ```

Add cclip to your path if desired.

### Configure cclip
1. Copy config file from `[path-to-cclip-repo]` to `~/.cclip.yaml`
    ```
    cp ~[path-to-cclip-repo]/cclip.yaml ~/.cclip.yaml
    ```
2. Add your custom values to `.cclip.yaml`:
    1. `pwd` - custom passphrase that will be used to perform client-side encryption on cclip data
    2. `bucket` - s3 bucket where cclip data will be stored
    3. `key` - file name under which cclip data will be written
    4. `aws-profile` - name of the AWS CLI Profile that you configured above

### Using cclip
#### Copy Text to Cloud Clipboard
```
cclip put "my clipboard data"
```
#### Retrieve Text from Cloud Clipboard
```
cclip get
```

### Troubleshooting

#### gnupg Errors
If you encounter errors related to `gnupg` while trying to use cclip, such as 
  > gnupghome should be a directory (it isn't)

you should be able to resolve by creating `~.gnupg` as follows:
  ```
  gpg -c anything-at-all
  ```
which will create the initial `~.gnupg` directory and some other prerequesite files.
