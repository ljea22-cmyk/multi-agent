import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent

NOTICE_PATH = ROOT / 'sample_notices.txt'
OUTPUT_SUMMARY = ROOT / 'output.md'
OUTPUT_USER = ROOT / 'output_user_guide.md'
REVIEW = ROOT / 'review_report.md'


def load_notices(path):
    return path.read_text(encoding='utf-8')


def split_notices(text):
    blocks = [b.strip() for b in re.split(r"\n\s*\n\s*\n+", text) if b.strip()]
    # also split on double-newline if needed
    if len(blocks) == 1:
        blocks = [b.strip() for b in re.split(r"\n\n", text) if b.strip()]
    return blocks


def extract_fields(block):
    lines = block.splitlines()
    title = lines[0].strip() if lines else ''
    data = {'title': title, 'targets': '', 'period': '', 'items': '', 'content': ''}
    for ln in lines[1:]:
        if ':' in ln:
            k, v = ln.split(':', 1)
            k = k.strip().lower()
            v = v.strip()
            if '대상' in k:
                data['targets'] = v
            elif '기간' in k:
                data['period'] = v
            elif '준비' in k:
                data['items'] = v
            elif '내용' in k:
                data['content'] += v + ' '
            else:
                # unknown key -> append to content
                data['content'] += ln + ' '
        else:
            data['content'] += ln + ' '
    return data


def normalize_period(p):
    # very simple normalization: extract dates like YYYY-MM-DD or YYYY-MM-DD ~ YYYY-MM-DD
    if not p:
        return None
    m = re.search(r"(\d{4}-\d{2}-\d{2})(?:\s*~\s*(\d{4}-\d{2}-\d{2}))?", p)
    if m:
        start = m.group(1)
        end = m.group(2) or m.group(1)
        return (start, end)
    # try single date like 2026-05-10 in content
    m2 = re.search(r"(\d{4}-\d{2}-\d{2})", p)
    if m2:
        return (m2.group(1), m2.group(1))
    return None


def classify_targets(target_text):
    if not target_text:
        return ['unknown']
    text = target_text.lower()
    groups = []
    if '모든' in text or '전체' in text:
        groups.append('all_students')
    if '1학년' in text or '신입' in text:
        groups.append('freshmen')
    if '대학원' in text or '대학원생' in text:
        groups.append('graduate_students')
    if '교수' in text:
        groups.append('professors')
    if not groups:
        groups.append(text)
    return groups


def render_summary(notices):
    lines = ["| 제목 | 대상 | 기간 | 준비물 |", "|---|---|---|---|"]
    for n in notices:
        period = n.get('period_norm')
        period_s = f"{period[0]} ~ {period[1]}" if period else n.get('period','')
        lines.append(f"| {n['title']} | {n['targets']} | {period_s} | {n['items']} |")
    OUTPUT_SUMMARY.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Wrote summary to {OUTPUT_SUMMARY}")


def render_user_guides(notices):
    by_group = {}
    for n in notices:
        groups = classify_targets(n['targets'])
        for g in groups:
            by_group.setdefault(g, []).append(n)
    out = []
    for g, items in by_group.items():
        out.append(f"## 대상: {g}\n")
        for it in items:
            period = it.get('period_norm')
            period_s = f"{period[0]} ~ {period[1]}" if period else it.get('period','')
            guide = f"- {it['title']}: 일정 {period_s}. 준비물: {it['items']}. {it.get('content','').strip()}"
            out.append(guide)
        out.append('\n')
    OUTPUT_USER.write_text('\n'.join(out), encoding='utf-8')
    print(f"Wrote user guides to {OUTPUT_USER}")


def write_review(reviews):
    if not reviews:
        Path(REVIEW).write_text('')
        return
    Path(REVIEW).write_text('\n'.join(reviews), encoding='utf-8')
    print(f"Wrote review report to {REVIEW}")


def main():
    if not NOTICE_PATH.exists():
        print('sample_notices.txt not found')
        return
    text = load_notices(NOTICE_PATH)
    blocks = split_notices(text)
    notices = []
    reviews = []
    for b in blocks:
        f = extract_fields(b)
        p = normalize_period(f.get('period',''))
        f['period_norm'] = p
        # simple validation
        if not f.get('targets'):
            reviews.append(f"[WARN] 대상 미기재: {f.get('title')}")
        if not p:
            reviews.append(f"[WARN] 기간 미파싱: {f.get('title')} - raw: {f.get('period')}")
        notices.append(f)
    render_summary(notices)
    render_user_guides(notices)
    write_review(reviews)
    print('Done')


if __name__ == '__main__':
    main()
