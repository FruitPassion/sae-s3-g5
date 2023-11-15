def convert_to_dict(posts):
    post_list = []
    if str(type(posts)) == "<class 'sqlalchemy.engine.row.Row'>":
        post_list = posts._asdict()
    else:
        for post in posts:
            post_list.append(post._asdict())
    return post_list
