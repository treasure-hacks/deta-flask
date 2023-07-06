import json
import os
import datetime
from urllib import request, error
import http.client
from deta import Base


todos = Base("todos")


def get_tasks() -> list[dict]:
    last = True
    tasks = []
    while last and len(tasks) < 10:
        # Since Deta Actions are in UTC time, you may need to fetch "tomorrow's tasks" if
        # you are a day ahead when you want your notifications to be sent.
        # tomorrow = datetime.date.today() + datetime.timedelta(1)
        response = todos.fetch({'date': datetime.date.today().isoformat()})
        tasks.extend(response.items)
        last = response.last
    return tasks


def create_embed(task: dict) -> dict:
    """Creates an embed for a task"""
    return {'title': task['key'], 'description': task['desc'], 'color': 0x73AD21}


def notify_discord() -> None:
    tasks = get_tasks()
    if not tasks:
        return

    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    headers = {'User-Agent': 'discord-webhook', 'Content-Type': 'application/json'}
    data = bytes(json.dumps({
        'content': 'Here are your todos for today:',
        'embeds': [create_embed(t) for t in tasks]
    }), 'utf-8')

    req = request.Request(webhook_url, data, method = 'POST', headers = headers)

    try:
        response: http.client.HTTPResponse = request.urlopen(req)
    except error.HTTPError as err:
        return print('Unable to notify user via Discord:', err.read())

    response.read()
