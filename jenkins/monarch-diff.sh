#!/bin/bash

set -e

REMOTE_SERVER="monarch-ttl-prod"
export timestamp=$(date +%Y%m%d%H%M)
directory=data-diff-"${timestamp}"
mkdir $directory
cd data-diff-"${timestamp}"

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install requests markdown

python3 ../../monarch/monarch-data-diff.py --config ../../conf/monarch-qc.json --threshold 10
deactivate

grep SEVERE /var/lib/jenkins/jobs/load-scigraph-data-on-dev/lastSuccessful/log | perl -e '$pos; while(<>){chomp; if ($_ =~ m/.*clique.*/){ $pos = 1;} elsif ($pos == 1){ $_ =~ s/SEVERE: //; print "\n$_"; $pos=2;} elsif($pos == 2){ $_ =~ s/SEVERE: //; print "\t$_";}}' | sed '/^$/d' > clique-warnings.tsv


scp -r ./$directory monarch@$REMOTE_SERVER:/var/www/data/qc/