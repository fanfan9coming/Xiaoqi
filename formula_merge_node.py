import json

async def main(args: Args) -> Output:
    candidates_fjx = args.params.get('candidates_fjx', '[]').strip()
    candidates_sh = args.params.get('candidates_sh', '[]').strip()
    candidates_jg = args.params.get('candidates_jg', '[]').strip()

    # 从每个来源库各取 top 2，不合并排序，直接整理成简洁列表
    summary = []

    for raw, label in [
        (candidates_fjx, '方剂学'),
        (candidates_sh, '伤寒论'),
        (candidates_jg, '金匮要略'),
    ]:
        if not raw:
            continue
        try:
            items = json.loads(raw)
        except:
            continue
        if not isinstance(items, list) or not items:
            continue
        # 取该来源 top 2
        for item in items[:2]:
            summary.append({
                '方名': item.get('方名', ''),
                '来源库': label,
                '出处': item.get('出处', ''),
                'score': item.get('score', 0),
                '命中': item.get('hit_count', 0),
                '组成': item.get('组成', ''),
            })

    # 按 score 降序
    summary.sort(key=lambda x: x['score'], reverse=True)

    if not summary:
        return {
            'candidates_brief': '无匹配',
            'top_formula_name': '',
            'top_source': '',
        }

    top = summary[0]

    # 生成简洁文本给 LLM
    lines = []
    for i, s in enumerate(summary, 1):
        lines.append(f"{i}. {s['方名']}（{s['来源库']}，{s['出处']}）score={s['score']} 命中{s['命中']}味 | 组成：{s['组成']}")

    return {
        'candidates_brief': '\n'.join(lines),
        'top_formula_name': top['方名'],
        'top_source': top['来源库'],
    }
