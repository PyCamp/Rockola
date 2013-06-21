source bin/activate
pip install -r requirements.txt
cd msgs_queue/
python setup.py install
cd ..

if tmux has-session -t rockola 2> /dev/null
then
  echo "WARN: The tmux session is already open."
else
  tmux start-server
  tmux new-session -d -s rockola -n cyclone
  tmux new-window -t rockola:1 -n flask
  tmux new-window -t rockola:2 -n shiva
  tmux new-window -t rockola:3 -n votesengine
fi

tmux send-keys -t rockola:2 "cd ~/shiva-server; source .virtualenv/bin/activate; shiva-server" C-m
tmux send-keys -t rockola:0 "source bin/activate; twistd -n cyclone-sse --amqp-host=192.168.10.90 -l 0" C-m
sleep 2
tmux send-keys -t rockola:1 "source bin/activate; gunicorn -k gevent -b 0.0.0.0:5000 --debug app:app" C-m
tmux send-keys -t rockola:3 "source bin/activate; cd votesengine; python votesengine.py" C-m

tmux select-window -t rockola:1
tmux attach-session -d -t rockola
