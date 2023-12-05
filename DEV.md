
# Troubleshooting

## Address already in use

If you get the following error when you run `chainlit run aipreneuros.py`
```
[Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

This means you have chainlit already running in the background at this time. You can check this with `ps aux | grep chainlit` To fix this, you can kill that process with:
```
pkill -9 -f chainlit
```
