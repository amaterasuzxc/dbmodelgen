#!/bin/bash
exec uvicorn main:app --port 8080 --host 0.0.0.0