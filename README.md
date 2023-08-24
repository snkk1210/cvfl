cvfl
=========

## これは何？

SSL 証明書の整合性をチェックできる WEB ツールです。  

## Installation

### 0. 必要なパッケージ 導入

```
sudo yum groupinstall "Development tools" -y
sudo yum install zlib-devel openssl-devel sqlite-devel libffi-devel -y
```

### 1. pyenv 導入

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

### 2. pyenv-virtualenv 導入

```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec $SHELL -l
```

### 3. 3.7 系 Python 導入

```
pyenv install 3.7.17
pyenv global 3.7.17
```

### 4. AWS CLI 導入

```
pip3 install -U pip
pip3 install awscli
aws configure
```

### 5. ソース 取得

```
pyenv virtualenv 3.10.12 venv
git clone https://github.com/snkk1210/cvfl.git
cd cvfl
cp -p .env.example .env
pyenv local venv
```

### 6. OpenSSL バイナリ　導入

```
sudo docker build -t al2 .
sudo docker run --detach --name tmp al2
sudo docker cp tmp:/usr/bin/openssl ./bin/
```

### 7. モジュール 導入

```
pip3 install -U pip
pip3 install flask
pip3 install zappa
pip3 install python-dotenv
```

### 8. デプロイ

- 通常

```
zappa init
===========================================================================
What do you want to call this environment (default 'dev'): dev
===========================================================================
zappa deploy
````

- カスタムドメインを使う場合

zappa_settings.json に下記フィールドを追記
```
        "domain": "xxxxxxxxx",
        "certificate_arn": "arn:aws:acm:us-east-1:xxxxxxxxx:certificate/xxxxxxxxx",
        "endpoint_configuration": ["REGIONAL"],
        "route53_enabled": false,
```

.env を下記に書き換え
```
ENV='/'
```

```
zappa deploy
zappa certify
```

- 接続元 IP アドレスを絞る場合

zappa_settings.json に下記フィールドを追記
```
       "apigateway_policy": "apigateway_policy.json",
```

ポリシーのテンプレート作成
```
cp -p ./.apigateway_policy.json.example ./apigateway_policy.json
```

apigateway_policy.json の下記フィールドに接続元 IP アドレスを追記
```
          "aws:SourceIp": [
            "xx.xx.xx.xx/32"
          ]
```

```
zappa deploy
```