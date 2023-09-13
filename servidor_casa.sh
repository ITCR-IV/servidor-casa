#!/bin/sh

# SysVinit script para iniciar el servidor_casa
# Asume que está instalado en el HOME de root en un directorio servidor_casa

ROOT_HOME=$(getent passwd | grep root | cut -d: --fields=6)

check_root() {
	if [ "$(id -u)" != "0" ]; then
		echo "This script must be run as root" 1>&2
		exit 1
	fi
}

# Check if the server is already running
is_running() {
	pgrep -f "python3 servidor_casa.py" > /dev/null
	return $?
}

start() {
	if is_running; then
		echo "Server is already running."
	else
		echo "Starting server..."
		cd "$ROOT_HOME"/servidor_casa
		python3 servidor_casa.py &
		echo "Server started."
	fi
}

stop() {
	if is_running; then
		echo "Stopping server..."
		pkill -f "python3 servidor_casa.py"
		echo "Server stopped."
	else
		echo "Server is not running."
	fi
}

case "$1" in
	start)
		check_root
		start
		;;
	stop)
		check_root
		stop
		;;
	restart)
		check_root
		stop
		start
		;;
	*)
		echo "Usage: $0 {start|stop|restart}"
		exit 1
		;;
esac

exit 0
