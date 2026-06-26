#!/bin/bash
cd "/Users/bytedance/Documents/Slidev-PPT/Clip" || exit 1
echo "Starting Slidev: AgentLoop.md ..."
exec ./node_modules/.bin/slidev AgentLoop.md --open
