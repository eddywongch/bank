
#!/bin/sh
#
# Eddy Wong
# eddy.wong@datastax.com
# Mar 24, 2021

# Loads csv files to a graph/keyspace
#
# Usage
#
# load_csv.sh [target graph] 
#
# Examples:
# > load_csv.sh mtb1
# 
# > load_csv.sh

DSBULK_HOME=/home/automaton/dsbulk/dsbulk-1.7.0/
DSBULK_EXE=$DSBULK_HOME/bin/dsbulk

# GRAPH is the graph/keyspace to load to
GRAPH=$1

if [ -z "$GRAPH" ]; then
    	#echo "Base dir must be provided"
	# Setting detault to 'mtb'
	GRAPH=mtb
fi

$DSBULK_EXE load -g $GRAPH -v Account -url Account.csv -header true
$DSBULK_EXE load -g $GRAPH -v Party -url Party.csv -header true
$DSBULK_EXE load -g $GRAPH -e owns -from Party -to Account -url owns.csv -header true
$DSBULK_EXE load -g $GRAPH -v Company -url Company.csv -header true
$DSBULK_EXE load -g $GRAPH -e works_for -from Party -to Company -url works_for.csv -header true

$DSBULK_EXE load -g $GRAPH -v Transaction -url Transaction.csv -header true
$DSBULK_EXE load -g $GRAPH -e withdraws_from -from Transaction -to Account -url withdraws_from.csv -header true
$DSBULK_EXE load -g $GRAPH -e deposits_to -from Transaction -to Account -url deposits_to.csv -header true

$DSBULK_EXE load -g $GRAPH -v Email -url Email.csv -header true
$DSBULK_EXE load -g $GRAPH -e uses_email -from Party -to Email -url uses_email.csv -header true

$DSBULK_EXE load -g $GRAPH -v Phone -url Phone.csv -header true
$DSBULK_EXE load -g $GRAPH -e uses_phone -from Party -to Phone -url uses_phone.csv -header true

$DSBULK_EXE load -g $GRAPH -v Address -url Address.csv -header true
$DSBULK_EXE load -g $GRAPH -e resides_at -from Party -to Address -url resides_at.csv -header true
