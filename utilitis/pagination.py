from urllib.parse import urlencode


def get_pager(url, total, page=1, per_page=12, url_args=None):
    url_args = url_args or {}
    page = int(page) if str(page).isdigit() else 1

    total_pages = max(1, -(-total // per_page))
    page = max(1, min(page, total_pages))

    offset = (page - 1) * per_page
    start = offset + 1 if total else 0
    end = min(offset + per_page, total)

    # ===== Extra filter values ke query string e convert kora (generic) =====
    clean_args = {k: v for k, v in url_args.items() if v}
    extra_qs = urlencode(clean_args)

    return {
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'total': total,
        'total_pages': total_pages,
        'start': start,
        'end': end,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'pages': list(range(1, total_pages + 1)),
        'url': url,
        'url_args': url_args,
        'extra_qs': extra_qs,   # notun field
    }