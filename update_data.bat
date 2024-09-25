@REM 从google excel中抽取数据
python extract_title_v4.py
python extract_data_v4.py
python merge_data_v3.py

@REM 将更新的数据提交到github仓库
git add .
git status
git commit -m "update data - Script auto push"
git status
git push -u origin main

@REM 等待输入后再关闭控制台
set /p=