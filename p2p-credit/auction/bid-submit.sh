#!/bin/bash

echo

#
# parameter list
#

WAIT="${1-5.000}"          # or "0.125"
echo "\$1: WAIT=$WAIT seconds"
HOST="${2-localhost:8000}" # or "p2p-credit.localhost:8000/"
echo "\$2: HOST=$HOST"
ACID="${3-1}"              # auction-id
echo "\$3: ACID=$ACID (auction-id)"
UIDs="${4-$(seq 3)}"       # or "1 2 3 4" etc.
echo "\$4: UIDs=$(echo $UIDs | sed -e "s/\n//g")"
MINA="${5-001}"
echo "\$5: MIN(amount)=$MINA"
MAXA="${6-125}"
echo "\$6: MAX(amount)=$MAXA"
MINR="${7-000.00}"
echo "\$7: MIN(rate)=$MINR%"
MAXR="${8-100.00}"
echo "\$8: MAX(rate)=$MAXR%"

echo

while [ 1 ] ; do for ID in $UIDs ; do curl "http://$HOST/auction/post/BID/?user-id=$ID&auction-id=$ACID&amount=$(($MINA+$RANDOM%(1+$MAXA-$MINA)))&rate=$(echo "scale=2; $MINR+($MAXR-$MINR)*$RANDOM / 32767" | bc)" ; sleep "$WAIT" ; done ; done

