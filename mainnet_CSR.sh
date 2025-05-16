bp=$(/root/.local/share/solana/install/active_release/bin/solana block-production --url https://api.mainnet-beta.solana.com --output json-compact)
totalBlocksProduced=$(echo $bp |jq -r '.total_slots')
totalSlotsSkipped=$(echo $bp | jq -r '.total_slots_skipped')
if [ -n "$totalBlocksProduced" ]; then
	pctTotSkipped=$(echo "scale=2 ; 100 * $totalSlotsSkipped / $totalBlocksProduced" | bc)
else 
	pctTotSkipped=0
fi

echo $pctTotSkipped
