#!/bin/bash
cd "/Users/bytedance/Documents/Slidev-PPT/Clip" || exit 1
echo "==> 清理可能残留的 git 锁 ..."
rm -f .git/index.lock
echo "==> 暂存工作区内容 ..."
git add AgentLoop.md AgentLoop.pdf MemLineage.md style.css public/image "王宇哲-20260415.pdf" 2>/dev/null
git add -u 2>/dev/null
echo "==> 提交 ..."
git commit -m "snapshot: 保存 AgentLoop/MemLineage 等工作区内容（动态化改造前）"
echo ""
echo "================ 最近提交记录 ================"
git log --oneline -5
echo ""
echo "✅ 完成。可以按 Cmd+W 关闭本窗口。"
