cvfl
=========

## What is this ?

SSL/TLS 証明書の整合性をチェックする WEB ツールです。  
AWS 上に API Gateway + Lambda のコンポーネントを使ってデプロイできる他、 Docker を使ってローカルで起動することも可能です。  
※ ローカルで起動する場合は [こちら](https://github.com/snkk1210/cvfl/tree/master/docker)

## Installation

### 1. Dependent Package Installation

```
sudo dnf groupinstall "Development tools" -y
sudo dnf install zlib-devel openssl-devel sqlite-devel libffi-devel -y
```

### 2. Building a Python environment 

- pyenv

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

- pyenv-virtualenv

```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec $SHELL -l
```

- Python

```
pyenv install 3.10.12
pyenv global 3.10.12
```

- AWS CLI

```
pip3 install -U pip
pip3 install awscli
aws configure
```

### 3. Get Source Code

```
pyenv virtualenv 3.10.12 venv
git clone https://github.com/snkk1210/cvfl.git
cd cvfl
cp -p .env.example .env
pyenv local venv
```

```
pip3 install -U pip
pip3 install -r requirements.txt
```

## Deploy ( AWS )

```
zappa init
===========================================================================
What do you want to call this environment (default 'dev'): dev
===========================================================================
```

### General

```
zappa deploy
````

### When using a custom domain

- Add the following fields to ```zappa_settings.json```
```
        "domain": "xxxxxxxxx",
        "certificate_arn": "arn:aws:acm:us-east-1:xxxxxxxxx:certificate/xxxxxxxxx",
        "endpoint_configuration": ["REGIONAL"],
        "route53_enabled": false,
```

- Rewrite ```.env``` as follows
```
ENV='/'
```

```
zappa deploy
zappa certify
```

### When narrowing down the source IP address

- Add the following fields to ```zappa_settings.json```
```
       "apigateway_policy": "apigateway_policy.json",
```

- Create a file based on a template
```
cp -p ./.apigateway_policy.json.example ./apigateway_policy.json
```

- Add the source IP address to the following field in ```apigateway_policy.json```
```
          "aws:SourceIp": [
            "xx.xx.xx.xx/32"
          ]
```

```
zappa deploy
```

## Usage

Select a Certificate, Private key, and Inter Cert, and press "Execute".  
If the expiration date is displayed, the integrity of the certificate is maintained.