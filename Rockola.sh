
if tmux has-session -t rockola 2> /dev/null
then
  echo "WARN: The tmux session is already open."
else
  tmux start-server
  tmux new-session -d -s rockola -n cyclone
  tmux new-window -t rockola:1 -n flask
  tmux new-window -t rockola:2 -n shiva
fi

tmux send-keys -t rockola:2 "cd ~/shiva-server; source .virtualenv/bin/activate; shiva-server" C-m
tmux send-keys -t rockola:0 "source bin/activate; twistd -n cyclone-sse --amqp-host=192.168.10.90 -l 0" C-m
sleep 2
tmux send-keys -t rockola:1 "source bin/activate; python app.py" C-m

tmux select-window -t rockola:1
tmux attach-session -d -t rockola
