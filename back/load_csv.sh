
#!/bin/sh
#
# Eddy Wong
# eddy.wong@datastax.com
# Created: Mar 24, 2021
# Updated: Aug 18, 2022

# Loads csv files to a graph/keyspace
#
# Usage
#
# load_csv.sh [target graph] 
#
# Examples:
# > load_csv.sh bank
# 
# > load_csv.sh

# Loacation  of DSBulk
DSBULK_HOME=/home/automaton/dsbulk/dsbulk-1.8.0
DSBULK_EXE=$DSBULK_HOME/bin/dsbulk

# Hardcoding to my dev server
HOST=54.148.138.237
PORT=9042

# Astra
#  Dsbulk upload csv
# /Users/eddy.wong/programs/dsbulk-1.8.0/bin/dsbulk load 
# -url /Users/eddy.wong/workspace/datastax/astra/bank/Account.csv 
# -k bank -t "Account" 
# -b /Users/eddy.wong/keys/secure-connect-ds5-poc.zip 
# -u DEeyDlsUfdMWrWgDdETwSZtS 
# -p  pAvGQUZnKoqBdwNtqXm7Ucneu5,ZcvpDrUaXCRvGlHjXY5O0CR9KNdnwD8S8SX8eQ7.1F_xeEW77hjAlHo25ZQIhuBexIfGlD6Q6IlLONr779t+8D_Gjf5EHZprI+5mg 
# -header true

# Astra stuff
BUNDLE=/Users/eddy.wong/keys/secure-connect-ds5-poc-plus.zip
#USERNAME=DEeyDlsUfdMWrWgDdETwSZtS
#PASSWORD=pAvGQUZnKoqBdwNtqXm7Ucneu5,ZcvpDrUaXCRvGlHjXY5O0CR9KNdnwD8S8SX8eQ7.1F_xeEW77hjAlHo25ZQIhuBexIfGlD6Q6IlLONr779t+8D_Gjf5EHZprI+5mg 
USERNAME=test
PASSWORD=test


# GRAPH is the graph/keyspace to load to
GRAPH=$1

if [ -z "$GRAPH" ]; then
    	#echo "Base dir must be provided"
	# Setting detault to 'bank'
	GRAPH=bank
fi

# ASTRA Flags like secure bundle. Use for loading into Artemis
if [ -z "$ASTRA" ]; then
	SCB_FLAGS=
else
	SCB_FLAGS=`echo "$SCB_FLAGS -u $USERNAME -p $PASSWORD"`
fi


echo "$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS -g $GRAPH -v "Account" -url Account.csv  -header true"
echo "FLAGS: $SCB_FLAGS"
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS -g $GRAPH -v "Account" -url Account.csv  -header true

$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS  -g $GRAPH -v Party -url Party.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS  -g $GRAPH -e owns -from Party -to Account -url owns.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS  -g $GRAPH -v Company -url Company.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS  -g $GRAPH -e works_for -from Party -to Company -url works_for.csv -header true

$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -v Transaction -url Transaction.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -e withdraws_from -from Transaction -to Account -url withdraws_from.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -e deposits_to -from Transaction -to Account -url deposits_to.csv -header true

$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -v Email -url Email.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -e uses_email -from Party -to Email -url uses_email.csv -header true

$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -v Phone -url Phone.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -e uses_phone -from Party -to Phone -url uses_phone.csv -header true

$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -v Address -url Address.csv -header true
$DSBULK_EXE load -h $HOST -p $PORT $SCB_FLAGS   -g $GRAPH -e resides_at -from Party -to Address -url resides_at.csv -header true
