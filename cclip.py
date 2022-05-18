#!/usr/bin/env python3

# TODO support file direction https://stackoverflow.com/questions/59829848/supply-either-stdin-or-a-file-pathname-option-to-python-click-cli-script


import boto3
import click
import gnupg
import logging
import os
import pyperclip
import time
import yaml


from botocore.exceptions import ClientError


logging.basicConfig(level=logging.ERROR)
gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'))
with open(os.path.expanduser('~/.cclip.yaml'), 'r') as f:
    config = yaml.safe_load(f.read())
session = boto3.Session(profile_name=config['aws-profile'])
s3 = session.client('s3')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('content')
def put(content):
    _put(content)


@cli.command()
def grab():
    _put(pyperclip.paste())


@cli.command()
def get():
    try:
        resp = s3.get_object(Bucket=config['bucket'], Key=config['key'])
        s3_data = resp['Body'].read()
        decrypted_data = gpg.decrypt(s3_data, passphrase=config['pwd'])
        data = yaml.safe_load(decrypted_data.data)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            logging.info('No cclip object found.')
        return
    for k in reversed(list(data.keys())):
        click.echo(data[k])


def _put(content):
    try:
        resp = s3.get_object(Bucket=config['bucket'], Key=config['key'])
        s3_data = resp['Body'].read()
        decrypted_data = gpg.decrypt(s3_data, passphrase=config['pwd'])
        data = yaml.safe_load(decrypted_data.data)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            logging.info('No cclip object found, creating new object.')
        data = {}
    if len(data.keys()) >= 10:
        data.pop(list(data.keys())[0], None)
    data[str(int(time.time()))] = content
    updated = yaml.dump(data)
    encrypted_data = gpg.encrypt(
        updated,
        recipients=None,
        symmetric=True,
        passphrase=config['pwd']
    )
    s3.put_object(
        Bucket=config['bucket'],
        Key=config['key'],
        Body=encrypted_data.data
    )


if __name__ == '__main__':
    cli()
