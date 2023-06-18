if [ -z ${PORT+x} ]; then
    PORT=8080
fi

uvicorn backend.main:app --host "0.0.0.0" --port ${PORT}