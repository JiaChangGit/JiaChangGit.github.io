# GitHub Pages 建置紀錄

2026-09-09：自訂 Pages workflow 在安裝 Bundler 時失敗。Gemfile.lock 指定
Bundler 2.6.7，最低需要 Ruby 3.1.0；workflow 卻固定 Ruby 3.0，實際為 3.0.7。
本機 Ruby 3.3.8 建置成功，不能證明不同 Ruby 版本的 CI 可以通過。
失敗紀錄：https://github.com/JiaChangGit/JiaChangGit.github.io/actions/runs/34142318247

Ruby 系列以 .ruby-version 與 workflow 的 setup-ruby 設定為共同來源；Gemfile
不另外鎖定 Ruby 版本，Bundler 版本沿用 Gemfile.lock。修改任一版本時，一起檢查 Ruby、RubyGems 與已鎖定 gems
的相容性。不要手動改寫 lockfile 的 BUNDLED WITH 來掩蓋安裝問題。

Pages 使用 GitHub Actions 作為部署來源；不再同時以 main 分支啟動 legacy build。
修復完成必須檢查同一 commit 的報告驗證及部署 workflow 都成功，並確認部署
指向該 commit、線上頁面包含本次修改。HTTP 200 或舊的 Pages built 狀態不足以
證明所有 CI 通過。

本文件屬開發維護紀錄，不納入 NVMe 教材正文。
