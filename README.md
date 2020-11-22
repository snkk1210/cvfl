certificate_verify_flask_lambda
=========

## これは何？

SSL証明書の整合性をチェックするWEBツールです。  
AWSのlambdaにデプロイします。

## 使い方

### 0.必要なパッケージの導入

```
yum groupinstall "Development tools" -y
yum install zlib-devel openssl-devel sqlite-devel -y
```

### 1.pyenvの導入

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

### 2.pyenv-virtualenvの導入

```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec $SHELL -l
```

### 3.3.6系のpythonを導入

```
pyenv install 3.6.5
pyenv global 3.6.5
```

### 4.awscliの導入/設定

```
pip install -U pip
pip install awscli
aws configure
```

### 5.ソースの取得

```
pyenv virtualenv 3.6.5 lambda
git clone https://github.com/keisukesanuki/certificate_verify_flask_lambda.git 
cd certificate_verify_flask_lambda
pyenv local lambda
```

### 6.モジュールの導入

```
pip install -U pip
pip install flask
pip install zappa
```

### 7.lambdaにデプロイ

```
zappa init
===========================================================================
What do you want to call this environment (default 'dev'): certificateCheck
===========================================================================
zappa deploy
```
