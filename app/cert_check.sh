#!/bin/bash

# MEMO: 引数チェック
if [ $# != 3 ]; then
    echo "ERR:invalid argument"
    exit 1
fi

# MEMO: エラー出力関数
function checkExitCode(){
    if [ $? != 0 ]; then
        echo "ERR: ${1} status is not 0"
        exit 1
    fi
}

function isEmpty(){
    if [ -z $1 ]; then
        echo "ERR: ${2} is Empty"
        exit 1
    fi
}

# MEMO: 証明書ファイルの HASH 値 を出力
CERT_HASH=`openssl x509 -noout -modulus -in ${1} | md5sum 2> /dev/null`
checkExitCode "openssl x509 -noout -modulus -in ${1} | md5sum"
isEmpty ${CERT_HASH} "CERT_HASH"

KEY_HASH=`openssl rsa -noout -modulus -in ${2} | md5sum 2> /dev/null`
checkExitCode "openssl rsa -noout -modulus -in ${2} | md5sum"
isEmpty ${KEY_HASH} "KEY_HASH"

CERT_ISSUER_HASH=`openssl x509 -issuer_hash -noout -in ${1} 2> /dev/null`
checkExitCode "openssl x509 -issuer_hash -noout -in ${1}"
isEmpty ${CERT_ISSUER_HASH} "CERT_ISSUER_HASH"

CA_SUBJECT_HASH=`openssl x509 -subject_hash -noout -in ${3} 2> /dev/null`
checkExitCode "penssl x509 -subject_hash -noout -in ${3}"
isEmpty ${CA_SUBJECT_HASH} "CA_SUBJECT_HASH"

# MEMO: 証明書 HASH と 鍵ファイル HASH を比較
if [  "${CERT_HASH}" == "${KEY_HASH}" ]; then
    echo "CERT_HASH and KEY_HASH are OK"
else
    echo "CERT_HASH and KEY_HASH are NG"
    exit 1
fi

# MEMO: 証明書 issuer HASH と CAファイル subject HASH を比較
if [  "${CERT_ISSUER_HASH}" == "${CA_SUBJECT_HASH}" ]; then
    echo "CERT_ISSUER_HASH and CA_SUBJECT_HASH are OK"
else
    echo "CERT_ISSUER_HASH and CA_SUBJECT_HASH are NG"
    exit 1
fi

# MEMO: 証明書の期限を出力
openssl x509 -noout -dates -in ${1}
exit 0