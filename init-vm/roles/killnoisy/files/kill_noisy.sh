#!/bin/bash

ps aux | grep run_sysbench.sh | awk '{print $2}' | xargs kill -9
