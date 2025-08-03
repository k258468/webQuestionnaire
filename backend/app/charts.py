# app/charts.py
from __future__ import annotations
import csv
import os
from collections import Counter
from pathlib import Path
from typing import Iterable
from matplotlib.ticker import MaxNLocator

import matplotlib
matplotlib.use("Agg")  # サーバー描画
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ===== パス =====
BASE_DIR   = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
ADMIN_DIR  = STATIC_DIR / "admin"
ADMIN_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR     = BASE_DIR / "data"
STUDENT_CSV  = DATA_DIR / "student_results.csv"
TEACHER_CSV  = DATA_DIR / "teacher_results.csv"

# ===== 日本語フォント（自動設定）=====
def _pick_jp_font() -> fm.FontProperties | None:
    # 1) Debian + fonts-noto-cjk を想定
    fixed = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if Path(fixed).exists():
        return fm.FontProperties(fname=fixed)

    # 2) ファミリー名で探索
    families = ["Noto Sans CJK JP", "Noto Sans CJK", "Noto Sans JP",
                "IPAexGothic", "IPAGothic", "Meiryo"]
    for fam in families:
        try:
            path = fm.findfont(fam, fallback_to_default=False)
            if path and os.path.exists(path):
                return fm.FontProperties(fname=path)
        except Exception:
            pass

    # 3) ディスク走査
    for root in ("/usr/share/fonts", "/usr/local/share/fonts"):
        p = Path(root)
        if not p.exists():
            continue
        for fp in p.rglob("*Noto*CJ*K*Regular*"):
            try:
                return fm.FontProperties(fname=str(fp))
            except Exception:
                continue
    return None

_JP_FP = _pick_jp_font()
if _JP_FP is not None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [_JP_FP.get_name()]
plt.rcParams["axes.unicode_minus"] = False

# ===== 列名 → 画像ファイルキー =====
STU_KEYS = {
    "学年":         "grade",   # admin/chart_student_grade.png
    "活用意向":     "q1",      # admin/chart_student_q1.png
    "懸念（複数）": "q2",      # admin/chart_student_q2.png
    "対策の受容":   "q3",      # admin/chart_student_q3.png
}
TCH_KEYS = {
    "把握の有無":         "q1_check",
    "把握手段":           "q11_how",
    "活用方法":           "q12_use",
    "確認意向":           "q21_want",
    "確認したい理由":     "q211_reason",
    "確認したくない理由": "no_want_reason",  # スキップ
    "利点":               "q2_advantage",
    "懸念":               "q3_concern",
    "導入意向":           "q4_use",
    "導入しない理由":     "no_adopt_reason", # スキップ
}

# 自由記述などグラフ化しない列
STU_SKIP: set[str] = set()
TCH_SKIP: set[str] = {"確認したくない理由", "導入しない理由"}

# ; 区切りの多選択列
MULTI_VAL_COLUMNS = {
    "懸念（複数）",
    "把握手段", "活用方法", "確認したい理由", "利点", "懸念",
}

# ===== 値→日本語ラベルのマップ =====
LABEL_MAP = {
    "student": {
        "grade": {
            "B1":"学部1年","B2":"学部2年","B3":"学部3年","B4":"学部4年",
            "M1":"修士1年","M2":"修士2年","D1":"博士1年","D2":"博士2年","D3":"博士3年",
        },
        "q1": {"思う":"思う","思わない":"思わない"},
        "q2": {
            "accuracy":"予測の精度や信頼性",
            "privacy":"学生のプライバシー保護・データ利用",
            "workload":"教員の業務負担の増加",
            "transparency":"データ利用の透明性",
            "integration":"学内システム・ワークフローとの連携",
            "other":"その他",
        },
        "q3": {"はい":"はい","いいえ":"いいえ"},
    },
    "teacher": {
        "q1_check": {"している":"している","していない":"していない"},
        "q11_how": {
            "quiz":"小テストの実施","react":"授業中の質問・反応","report":"課題・レポート",
            "office":"オフィスアワー","direct":"直接相談・様子から判断","other":"その他",
        },
        "q12_use": {
            "material":"講義方針・資料の改善","exam":"期末テスト難易度調整",
            "assign":"課題量・難易度の調整","office":"オフィスアワーで活用","other":"その他",
        },
        "q21_want": {"したい":"したい","したくない":"したくない"},
        "q211_reason": {
            "no_method":"確認手段がない","no_time":"作成/採点の時間がない",
            "too_many":"受講者数が多すぎる","other":"その他",
        },
        # 利点：想定コード + 誤混入しがちな懸念コードも日本語化
        "q2_advantage": {
            "no_test":"テストやレポート作成なしで確認できる",
            "many_overview":"受講者が多くても一目で把握できる",
            "paperless":"紙媒体の必要がない",
            "quality":"講義の質がわかる",
            "everytime":"毎講義理解度確認ができる",
            "other":"その他",
            "accuracy":"予測の精度や信頼性",
            "privacy":"学生のプライバシー・データ利用",
            "workload":"教員の業務負担の増加",
            "transparency":"データ利用の透明性",
            "integration":"既存システム・ワークフローとの連携",
        },
        "q3_concern": {
            "accuracy":"予測の精度や信頼性",
            "privacy":"学生のプライバシー・データ利用",
            "workload":"教員の業務負担の増加",
            "transparency":"データ利用の透明性",
            "integration":"既存システム・ワークフローとの連携",
            "other":"その他",
        },
        "q4_use": {"思う":"思う","思わない":"思わない"},
    },
}

# ===== Utility =====
def _read_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _split_semicolon(values: Iterable[str]) -> Counter:
    c = Counter()
    for v in values:
        if not v:
            continue
        for part in str(v).split(";"):
            part = part.strip()
            if part:
                c[part] += 1
    return c

def _count_categorical(values: Iterable[str]) -> Counter:
    c = Counter()
    for v in values:
        v = (v or "").strip()
        if v:
            c[v] += 1
    return c

def _remap_counter(counter: Counter, label_map: dict[str, str]) -> Counter:
    out = Counter()
    for k, v in counter.items():
        out[label_map.get(k, k)] += v
    return out

def _bar(counter: Counter, save_to: Path):
    """カテゴリ頻度の棒グラフを保存（タイトル無し／日本語ラベル対応、y軸は整数目盛り）"""
    save_to.parent.mkdir(parents=True, exist_ok=True)

    if not counter:
        fig = plt.figure(figsize=(5, 3))
        plt.axis("off")
        fig.savefig(save_to, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return

    labels, counts = zip(*counter.most_common())

    fig = plt.figure(figsize=(6.8, 4.6))
    ax = fig.add_subplot(111)
    ax.bar(range(len(labels)), counts)
    ax.set_xticks(range(len(labels)))

    # x軸ラベル（日本語フォント）
    if _JP_FP is not None:
        ax.set_xticklabels(labels, rotation=30, ha="right", fontproperties=_JP_FP)
    else:
        ax.set_xticklabels(labels, rotation=30, ha="right")

    # ← y軸は整数のみ
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(counts) if max(counts) > 0 else 1)

    ax.tick_params(axis='y', which='both', length=0)
    fig.tight_layout()
    fig.savefig(save_to, dpi=160, bbox_inches="tight")
    plt.close(fig)

# ===== 学生 =====
def build_student_charts() -> list[dict]:
    rows = _read_rows(STUDENT_CSV)
    if not rows:
        for key in STU_KEYS.values():
            (ADMIN_DIR / f"chart_student_{key}.png").unlink(missing_ok=True)
        return []

    out: list[dict] = []
    for col, key in STU_KEYS.items():
        if col in STU_SKIP or col not in rows[0]:
            continue
        series  = [r.get(col, "") for r in rows]
        counter = _split_semicolon(series) if col in MULTI_VAL_COLUMNS else _count_categorical(series)
        # 日本語ラベルへ置換
        m = LABEL_MAP["student"].get(key)
        if m:
            counter = _remap_counter(counter, m)
        out_path = ADMIN_DIR / f"chart_student_{key}.png"
        _bar(counter, out_path)
        out.append({"col": col, "key": key, "file": f"admin/{out_path.name}"})
    return out

# ===== 教員 =====
def build_teacher_charts() -> list[dict]:
    rows = _read_rows(TEACHER_CSV)
    if not rows:
        for key in TCH_KEYS.values():
            (ADMIN_DIR / f"chart_teacher_{key}.png").unlink(missing_ok=True)
        return []

    out: list[dict] = []
    for col, key in TCH_KEYS.items():
        if col in TCH_SKIP or col not in rows[0]:
            continue
        series  = [r.get(col, "") for r in rows]
        counter = _split_semicolon(series) if col in MULTI_VAL_COLUMNS else _count_categorical(series)
        # 日本語ラベルへ置換
        m = LABEL_MAP["teacher"].get(key)
        if m:
            counter = _remap_counter(counter, m)
        out_path = ADMIN_DIR / f"chart_teacher_{key}.png"
        _bar(counter, out_path)
        out.append({"col": col, "key": key, "file": f"admin/{out_path.name}"})
    return out

# ===== 一括再生成 =====
def rebuild_all() -> dict:
    return {
        "student": build_student_charts(),
        "teacher": build_teacher_charts(),
    }

if __name__ == "__main__":
    print("JP font:", _JP_FP.get_name() if _JP_FP else None)
    print(rebuild_all())