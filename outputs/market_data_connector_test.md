# Market Data Connector Test

| ticker | current_price | market_cap | enterprise_value | shares_outstanding | price_change_6m | price_change_12m | ev_to_sales | price_to_sales | missing_fields_count |
|---|---|---|---|---|---|---|---|---|---|
| RKLB | 102.39 | 63975190528 | 65184362496 | 578867475 | 0.847861 | 3.02952 | 95.919 | 94.1396 | 1 |
| KTOS | 57.75 | 10829279232 | 9743524864 | 187519984 | -0.222327 | 0.382902 | 6.885 | 7.65212 | 0 |
| RDW | 15.12 | 3007651072 | 3446226688 | 198918728 | 1.19449 | -0.207547 | 9.29 | 8.10779 | 1 |
| MRCY | 120.3 | 7223207424 | 7489036288 | 60043283 | 0.614982 | 1.27067 | 7.745 | 7.47013 | 1 |
| IRDM | 47.32 | 5003036672 | 6954182656 | 105727744 | 1.68864 | 0.652235 | 7.94 | 5.71229 | 0 |

## Missing Fields
- `RKLB`: market_data.pe_ratio
- `KTOS`: none
- `RDW`: market_data.pe_ratio
- `MRCY`: market_data.pe_ratio
- `IRDM`: none

## Warnings
- `RKLB`: none
- `KTOS`: none
- `RDW`: none
- `MRCY`: none
- `IRDM`: none
