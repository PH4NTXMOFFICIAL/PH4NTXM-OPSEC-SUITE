#!/bin/bash

ALERT_DIR="/run/ph4ntxm-opsec-connwatch"
STATS_FILE="$ALERT_DIR/connwatch-stats.log"
ALERT_LOCK="$ALERT_DIR/connwatch-alert.lock"
ALERT_LOG="$ALERT_DIR/connwatch-alerts.history"

sudo mkdir -p "$ALERT_DIR"
sudo chmod 777 "$ALERT_DIR"
sudo touch "$STATS_FILE" "$ALERT_LOG"
sudo chmod 666 "$STATS_FILE" "$ALERT_LOG"

alert_sent=0
last_alert_time=-300
last_update=0
last_alert_hits=0

declare -A hit_count
declare -A ports_seen
declare -A ports_list

echo "PH4NTXM OPSEC CONNWATCH: Monitor Active..."

MY_IPS=$(hostname -I)
read -ra MY_IP_ARRAY <<< "$MY_IPS"

while read -r line; do

    SRC_RAW=$(echo "$line" | grep -oE 'IP [^ ]+' | awk '{print $2}')
    DEST_RAW=$(echo "$line" | grep -oE '> [^ ]+' | awk '{print $2}')

    [[ -z "$SRC_RAW" || -z "$DEST_RAW" ]] && continue

    SRC_IP=$(echo "$SRC_RAW" | rev | cut -d. -f2- | rev)
    DEST_IP=$(echo "$DEST_RAW" | rev | cut -d. -f2- | rev)

    PORT=$(echo "$DEST_RAW" | rev | cut -d. -f1 | rev | tr -d ':')
    [[ "$PORT" =~ ^[0-9]+$ ]] || continue

    IS_INBOUND=false
    for myip in "${MY_IP_ARRAY[@]}"; do
        [[ "$DEST_IP" == "$myip" ]] && IS_INBOUND=true && break
    done

    [[ "$IS_INBOUND" == false ]] && continue
    [[ "$SRC_IP" == "127.0.0.1" ]] && continue

    ((hit_count["$SRC_IP"]++))

    if [ "${hit_count["$SRC_IP"]}" -gt 50 ]; then
        current_time=$SECONDS
        
        if [[ $((current_time - last_alert_time)) -gt 300 ]] && [[ "${hit_count["$SRC_IP"]}" -gt "$last_alert_hits" ]]; then
            
            if [ ! -f "$ALERT_LOCK" ]; then
                alert_sent=1
                last_alert_time=$current_time
                last_alert_hits=${hit_count["$SRC_IP"]}
                
                touch "$ALERT_LOCK"
                chmod 666 "$ALERT_LOCK"
                
                echo "[ALERT] $SRC_IP exceeded threshold ($(date))" >> "$ALERT_DIR/connwatch-alerts.history"
                
                REAL_USER=$(who | grep '(:0)' | awk '{print $1}' | head -n1)
                [ -z "$REAL_USER" ] && REAL_USER=$(stat -c '%U' /dev/tty0 2>/dev/null)
                [ -z "$REAL_USER" ] && REAL_USER=$(logname 2>/dev/null || echo "$SUDO_USER")
                
                if [ -n "$REAL_USER" ]; then
                    USER_ID=$(id -u "$REAL_USER")
                    HOME_DIR=$(getent passwd "$REAL_USER" | cut -d: -f6)

                                                        sudo -u "$REAL_USER" \
            DISPLAY=:0 \
            XAUTHORITY="$HOME_DIR/.Xauthority" \
            DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$USER_ID/bus" \
            python3 - <<EOF &
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def on_click(button):
    path = "$ALERT_LOCK"
    if os.path.exists(path):
        os.remove(path)
    Gtk.main_quit()

win = Gtk.Window(title='PH4NTXM OpSec ConnWatch')
icon_path = "/usr/share/icons/Lyra-blue-dark/apps/scalable/ph4ntxm-opsec-connwatch.svg"
if os.path.exists(icon_path):
    win.set_icon_from_file(icon_path)

win.set_position(Gtk.WindowPosition.CENTER)
win.set_size_request(400, 100)
win.set_resizable(False)
win.set_keep_above(True)
win.set_border_width(10)

win.connect("destroy", lambda w: on_click(None))

vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
label = Gtk.Label()
label.set_markup('<span size="large" weight="bold" foreground="#ff4d5a">[SECURITY ALERT]</span>\n\n'
                 'High number of incoming connection attempts detected.\n'
                 'Check PH4NTXM OpSec ConnWatch for details.')
label.set_line_wrap(True)

btn = Gtk.Button(label='Close')
btn.connect('clicked', on_click)

vbox.pack_start(label, True, True, 2)
vbox.pack_start(btn, False, False, 2)
win.add(vbox)
win.show_all()
Gtk.main()
EOF
                fi
            fi
        fi
    fi

    key="$SRC_IP:$PORT"
    if [[ -z "${ports_seen[$key]}" ]]; then
        ports_seen[$key]=1
        ports_list[$SRC_IP]="${ports_list[$SRC_IP]}$PORT,"
    fi

    if [ "$SECONDS" -gt "$last_update" ]; then
        last_update=$SECONDS
        {
            echo "IP ADDRESS      | HITS | TARGET PORTS"
            echo "----------------|------|-------------------------"
            for addr in $(printf "%s\n" "${!hit_count[@]}" | sort -V); do
                ports=$(sed 's/,$//' <<< "${ports_list[$addr]}")
                ports="${ports:--}"
                [ "${#ports}" -gt 25 ] && ports="${ports:0:22}..."
                printf "%-15s | %4d | %s\n" "$addr" "${hit_count[$addr]}" "$ports"
            done
        } > "$STATS_FILE"
    fi

done < <(sudo tcpdump -l -U -i any -n "tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0" 2>/dev/null)
