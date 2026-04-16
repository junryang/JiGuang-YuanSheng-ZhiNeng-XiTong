# Day5 发布前最终检查清单（20260417）

## 文档定版结果

- Go/No-Go 评审纪要：`d:\BaiduSyncdisk\JiGuang\docs\D5_GO_NO_GO_REVIEW_MEMO_20260417_r1.md`
- 发布纪要：`d:\BaiduSyncdisk\JiGuang\docs\D3_RELEASE_MEMO_20260417_r1.md`
- 值班排班表：`d:\BaiduSyncdisk\JiGuang\docs\D5_RELEASE_DUTY_SCHEDULE_20260417_auto_filled.md`
- 工件锁定清单：`d:\BaiduSyncdisk\JiGuang\backend\reports\day5-artifact-lock-20260416-161958.json`

## 一键执行顺序

1. `python -m pytest -m day3_gate -q --tb=short`
2. `python scripts/day4_gate_runner.py --reports-dir "d:/BaiduSyncdisk/JiGuang/backend/reports"`
3. `python scripts/day5_release_prep.py --reports-dir "d:/BaiduSyncdisk/JiGuang/backend/reports" --output-dir "d:/BaiduSyncdisk/JiGuang/docs" --duty-schedule "d:/BaiduSyncdisk/JiGuang/docs/D5_RELEASE_DUTY_SCHEDULE_20260417_auto_filled.md" --emit-duty-todo`
4. `python scripts/day5_artifact_lock.py --release-tag "release-20260417-r1" --backend-digest "<真实digest>" --frontend-checksum "<真实checksum>" --output-dir "d:/BaiduSyncdisk/JiGuang/backend/reports"`

## 窗口前人工确认

- [ ] 主备联系方式实名校验
- [ ] 升级链路与响应 SLA 已确认
- [ ] 回滚入口可用并已演练
- [ ] Go/No-Go 评审签字完成
- [ ] 发布纪要签字完成
