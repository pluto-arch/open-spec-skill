param(
  [string]$HostName = "127.0.0.1",
  [int]$Port = 8765,
  [string]$LogFile = "docs/open-spec/telemetry/events.jsonl"
)

python .\skills\open-spec\scripts\workflow_monitor_server.py --host $HostName --port $Port --log-file $LogFile
