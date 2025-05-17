sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert")|.alert.signature'
