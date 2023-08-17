cvfl
=========

## これは何？

~~SSL 証明書の整合性をチェックする WEB ツールです。~~  
~~AWS Lambda にデプロイします。~~  
準備中

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

### 4. awscli 導入

```
pip3 install -U pip
pip3 install awscli
aws configure
```

### 5. ソース 取得

```
pyenv virtualenv 3.7.17 venv
git clone https://github.com/snkk1210/cvfl.git
cd cvfl
pyenv local venv
```

### 6. モジュール 導入

```
pip3 install -U pip
pip3 install flask
pip3 install zappa
```

### 7. Lambda デプロイ

```
zappa init
===========================================================================
What do you want to call this environment (default 'dev'): dev
===========================================================================
zappa deploy