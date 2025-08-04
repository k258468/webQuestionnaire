# app/charts.py
from __future__ import annotations
import csv
import os
from collections import Counter
from pathlib import Path
from typing import Iterable, Callable
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
    fixed = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if Path(fixed).exists():
        return fm.FontProperties(fname=fixed)
    families = ["Noto Sans CJK JP", "Noto Sans CJK", "Noto Sans JP",
                "IPAexGothic", "IPAGothic", "Meiryo"]
    for fam in families:
        try:
            path = fm.findfont(fam, fallback_to_default=False)
            if path and os.path.exists(path):
                return fm.FontProperties(fname=path)
        except Exception:
            pass
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

# ; 区切りの多選択列（これ以外は単一選択＝円グラフ）
MULTI_VAL_COLUMNS = {
    "懸念（複数）",
    "把握手段", "活用方法", "確認したい理由", "利点", "懸念",
}

# ===== 値→日本語ラベルのマップ（表示順は辞書定義順） =====
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

def _count_series(
    values: Iterable[str],
    multi: bool,
    normalizer: Callable[[str], str] | None = None,
) -> Counter:
    c = Counter()
    for raw in values:
        if not raw:
            continue
        parts = str(raw).split(";") if multi else [str(raw)]
        for p in parts:
            v = p.strip()
            if not v:
                continue
            if normalizer:
                v = normalizer(v)
            if v:
                c[v] += 1
    return c

def _remap_counter(counter: Counter, label_map: dict[str, str]) -> Counter:
    out = Counter()
    for k, v in counter.items():
        out[label_map.get(k, k)] += v
    return out

def _order_by_labelmap(counter: Counter, label_map: dict[str, str] | None):
    """表示順を label_map の定義順に合わせる（存在するもののみ）"""
    if not counter:
        return [], []
    if not label_map:
        labels, counts = zip(*counter.most_common())
        return list(labels), list(counts)
    ordered_labels: list[str] = []
    ordered_counts: list[int] = []
    jp_order = [v for v in label_map.values()]
    for lab in jp_order:
        if lab in counter:
            ordered_labels.append(lab)
            ordered_counts.append(counter[lab])
    for lab, cnt in counter.items():
        if lab not in ordered_labels:
            ordered_labels.append(lab)
            ordered_counts.append(cnt)
    return ordered_labels, ordered_counts

# ===== 正規化（丸め） =====
def _make_normalizer(role: str, key: str) -> Callable[[str], str] | None:
    # 学生
    if role == "student":
        if key == "q2":
            # other:xxx → other
            return lambda s: "other" if s.strip().startswith("other") else s.strip()
        if key == "q3":
            # 「いいえ」起点は全部「いいえ」に（いいえ:..., いいえ理由, 等）
            def _n(s: str) -> str:
                t = s.strip()
                return "いいえ" if ("いいえ" in t) else t
            return _n

    # 教員
    if role == "teacher":
        # 多選択は other:xxx → other
        if key in {"q11_how", "q12_use", "q211_reason", "q2_advantage", "q3_concern"}:
            return lambda s: "other" if s.strip().startswith("other") else s.strip()

        if key == "q21_want":
            # 「したくない」や「したくない理由…」を全て「したくない」へ
            def _n(s: str) -> str:
                t = s.strip()
                if "したくない" in t:
                    return "したくない"
                if "したい" in t:
                    return "したい"
                return t
            return _n

        if key == "q4_use":
            # 「思わない」や「思わない理由…」を全て「思わない」へ
            def _n(s: str) -> str:
                t = s.strip()
                if "思わない" in t:
                    return "思わない"
                if "思う" in t:
                    return "思う"
                return t
            return _n

    return None

# ===== 描画 =====
def _bar(labels: list[str], counts: list[int], save_to: Path):
    """棒グラフ（日本語フォント／y軸整数）"""
    save_to.parent.mkdir(parents=True, exist_ok=True)
    if not labels:
        fig = plt.figure(figsize=(6.8, 4.6))
        plt.axis("off")
        fig.savefig(save_to, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return
    fig = plt.figure(figsize=(6.8, 4.6))
    ax = fig.add_subplot(111)
    ax.bar(range(len(labels)), counts)
    ax.set_xticks(range(len(labels)))
    if _JP_FP is not None:
        ax.set_xticklabels(labels, rotation=30, ha="right", fontproperties=_JP_FP)
    else:
        ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(counts) if max(counts) > 0 else 1)
    ax.tick_params(axis='y', which='both', length=0)
    fig.tight_layout()
    fig.savefig(save_to, dpi=160, bbox_inches="tight")
    plt.close(fig)

def _pie(labels: list[str], counts: list[int], save_to: Path):
    """円グラフ（日本語フォント／小数なし%表示）"""
    save_to.parent.mkdir(parents=True, exist_ok=True)
    if not labels:
        fig = plt.figure(figsize=(6.8, 4.6))
        plt.axis("off")
        fig.savefig(save_to, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return
    fig = plt.figure(figsize=(6.8, 4.6))
    ax = fig.add_subplot(111)
    autopct = '%.0f%%'
    kw = {}
    if _JP_FP is not None:
        kw["textprops"] = {"fontproperties": _JP_FP}
    ax.pie(counts, labels=labels, autopct=autopct, startangle=90, counterclock=False, **kw)
    ax.axis('equal')
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
        if col not in rows[0] or col in STU_SKIP:
            continue
        multi = col in MULTI_VAL_COLUMNS
        normalizer = _make_normalizer("student", key)
        series = [r.get(col, "") for r in rows]
        counter = _count_series(series, multi=multi, normalizer=normalizer)
        m = LABEL_MAP["student"].get(key)
        if m:
            counter = _remap_counter(counter, m)
        labels, counts = _order_by_labelmap(counter, m)
        out_path = ADMIN_DIR / f"chart_student_{key}.png"
        if multi:
            _bar(labels, counts, out_path)
        else:
            _pie(labels, counts, out_path)
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
        if col not in rows[0] or col in TCH_SKIP:
            continue
        multi = col in MULTI_VAL_COLUMNS
        normalizer = _make_normalizer("teacher", key)
        series = [r.get(col, "") for r in rows]
        counter = _count_series(series, multi=multi, normalizer=normalizer)
        m = LABEL_MAP["teacher"].get(key)
        if m:
            counter = _remap_counter(counter, m)
        labels, counts = _order_by_labelmap(counter, m)
        out_path = ADMIN_DIR / f"chart_teacher_{key}.png"
        if multi:
            _bar(labels, counts, out_path)
        else:
            _pie(labels, counts, out_path)
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